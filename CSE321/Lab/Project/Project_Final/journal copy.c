#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <time.h>
#include <stdbool.h>

// ==========================================
// 1. CONSTANTS & STRUCTURES
// ==========================================

#define FS_MAGIC           0x56534653U
#define JOURNAL_MAGIC      0x4A524E4C
#define BLOCK_SIZE         4096U
#define INODE_SIZE         128U
#define JOURNAL_BLOCK_IDX  1U
#define JOURNAL_BLOCKS     16U
#define TOTAL_JOURNAL_SIZE (JOURNAL_BLOCKS * BLOCK_SIZE)
#define INODE_BLOCKS_CNT   2U  
#define MAX_TXN_RECORDS    64

#define REC_DATA   1
#define REC_COMMIT 2

struct superblock {
    uint32_t magic;
    uint32_t block_size;
    uint32_t total_blocks;
    uint32_t inode_count;
    uint32_t journal_block;
    uint32_t inode_bitmap;
    uint32_t data_bitmap;
    uint32_t inode_start;
    uint32_t data_start;
    uint8_t  _pad[128 - 9 * 4];
};
_Static_assert(sizeof(struct superblock) == 128, "Superblock size mismatch");

struct inode {
    uint16_t type;  // 0=free, 1=file, 2=dir
    uint16_t links;
    uint32_t size;
    uint32_t direct[8];
    uint32_t ctime;
    uint32_t mtime;
    uint8_t  _pad[128 - (2 + 2 + 4 + 8 * 4 + 4 + 4)];
};
_Static_assert(sizeof(struct inode) == 128, "Inode size mismatch");

struct dirent {
    uint32_t inode;
    char name[28];
};
_Static_assert(sizeof(struct dirent) == 32, "Dirent size mismatch");

struct journal_header {
    uint32_t magic;
    uint32_t nbytes_used;
};

struct rec_header {
    uint16_t type;
    uint16_t size;
};

struct data_record {
    struct rec_header hdr;
    uint32_t block_no;
    uint8_t data[BLOCK_SIZE];
};

struct commit_record {
    struct rec_header hdr;
};

// ==========================================
// 2. SAFE I/O & HELPERS
// ==========================================

void die(const char *msg) {
    perror(msg);
    exit(EXIT_FAILURE);
}

void *safe_malloc(size_t size) {
    void *p = malloc(size);
    if (!p) die("Memory allocation failed");
    return p;
}

void read_full(int fd, void *buf, size_t count, off_t offset) {
    char *ptr = (char *)buf;
    size_t remaining = count;
    while (remaining > 0) {
        ssize_t n = pread(fd, ptr, remaining, offset);
        if (n < 0) {
            if (errno == EINTR) continue;
            die("pread failed");
        }
        if (n == 0) die("pread: unexpected EOF");
        ptr += n;
        remaining -= n;
        offset += n;
    }
}

// FIX #7: Handle pwrite returning 0
void write_full(int fd, const void *buf, size_t count, off_t offset) {
    const char *ptr = (const char *)buf;
    size_t remaining = count;
    while (remaining > 0) {
        ssize_t n = pwrite(fd, ptr, remaining, offset);
        if (n < 0) {
            if (errno == EINTR) continue;
            die("pwrite failed");
        }
        if (n == 0) die("pwrite: short write (0 bytes)");
        ptr += n;
        remaining -= n;
        offset += n;
    }
}

void read_block(int fd, uint32_t block_idx, void *buf) {
    read_full(fd, buf, BLOCK_SIZE, (off_t)block_idx * BLOCK_SIZE);
}

void write_block(int fd, uint32_t block_idx, const void *buf) {
    write_full(fd, buf, BLOCK_SIZE, (off_t)block_idx * BLOCK_SIZE);
}

// FIX #5: Check against total_blocks and data region
bool is_valid_target_block(const struct superblock *sb, uint32_t block_no) {
    if (block_no == 0) return false; // Superblock
    if (block_no >= sb->journal_block && block_no < sb->journal_block + JOURNAL_BLOCKS) return false;
    if (block_no >= sb->total_blocks) return false; // Out of bounds
    return true;
}

// Helper to check if a block is part of the inode table
bool is_inode_table_block(const struct superblock *sb, uint32_t block_no) {
    return (block_no >= sb->inode_start && block_no < sb->inode_start + INODE_BLOCKS_CNT);
}

bool is_name_match(const char *entry_name, const char *search_name) {
    char safe_buf[29] = {0};
    memcpy(safe_buf, entry_name, 28);
    return strcmp(safe_buf, search_name) == 0;
}

void set_bit(uint8_t *bitmap, uint32_t index) {
    bitmap[index / 8] |= (1 << (index % 8));
}

int check_bit(const uint8_t *bitmap, uint32_t index) {
    return (bitmap[index / 8] >> (index % 8)) & 1;
}

// ==========================================
// 3. ROBUST REPLAY LOGIC
// ==========================================

void load_current_state(int fd, struct superblock *sb, 
                        uint8_t *inode_bitmap, 
                        uint8_t *inode_table_full, 
                        uint8_t *root_data_block,
                        uint32_t *current_root_data_blk_idx) 
{
    // Read Disk State
    read_block(fd, sb->inode_bitmap, inode_bitmap);
    for (uint32_t i = 0; i < INODE_BLOCKS_CNT; i++) {
        read_block(fd, sb->inode_start + i, inode_table_full + (i * BLOCK_SIZE));
    }
    
    // Validate root block index before reading (FIX #5)
    if (!is_valid_target_block(sb, *current_root_data_blk_idx)) {
        die("Corrupt root directory block index on disk");
    }
    read_block(fd, *current_root_data_blk_idx, root_data_block);

    // Read Journal
    uint8_t *journal_mem = safe_malloc(TOTAL_JOURNAL_SIZE);
    for (int i = 0; i < JOURNAL_BLOCKS; i++) {
        read_block(fd, sb->journal_block + i, journal_mem + (i * BLOCK_SIZE));
    }

    struct journal_header *j_hdr = (struct journal_header *)journal_mem;
    
    // FIX #2: Check if nbytes_used is garbage even if magic is correct
    if (j_hdr->magic != JOURNAL_MAGIC || 
        j_hdr->nbytes_used < sizeof(struct journal_header) || 
        j_hdr->nbytes_used > TOTAL_JOURNAL_SIZE) {
        free(journal_mem);
        return; 
    }

    // Replay
    uint32_t offset = sizeof(struct journal_header);
    struct data_record *pending_recs[MAX_TXN_RECORDS]; 
    int pending_count = 0;

    while (offset < j_hdr->nbytes_used) {
        if (offset + sizeof(struct rec_header) > TOTAL_JOURNAL_SIZE) break;

        struct rec_header *rh = (struct rec_header *)(journal_mem + offset);
        
        if (rh->type == REC_DATA && rh->size != sizeof(struct data_record)) break;
        if (rh->type == REC_COMMIT && rh->size != sizeof(struct commit_record)) break;
        if (rh->size == 0 || offset + rh->size > j_hdr->nbytes_used) break;

        if (rh->type == REC_DATA) {
            struct data_record *dr = (struct data_record *)rh;
            if (is_valid_target_block(sb, dr->block_no)) {
                // FIX #8: Abort on overflow
                if (pending_count >= MAX_TXN_RECORDS) {
                    fprintf(stderr, "Error: Transaction too large to replay.\n");
                    free(journal_mem); exit(EXIT_FAILURE);
                }
                pending_recs[pending_count++] = dr;
            }
        } 
        else if (rh->type == REC_COMMIT) {
            // FIX #6: Apply to buffers. Handle Root Block Change.
            
            // 1. First Pass: Apply Inode Bitmap and Inode Table updates
            for (int i = 0; i < pending_count; i++) {
                struct data_record *dr = pending_recs[i];
                if (dr->block_no == sb->inode_bitmap) {
                    memcpy(inode_bitmap, dr->data, BLOCK_SIZE);
                }
                else if (is_inode_table_block(sb, dr->block_no)) {
                    uint32_t relative_idx = dr->block_no - sb->inode_start;
                    memcpy(inode_table_full + (relative_idx * BLOCK_SIZE), dr->data, BLOCK_SIZE);
                }
            }

            // 2. Check if Root Inode Direct Pointer Changed
            struct inode *root_node = (struct inode *)inode_table_full;
            uint32_t next_root_blk = root_node->direct[0];
            bool root_moved = (next_root_blk != 0 && next_root_blk != *current_root_data_blk_idx);

            // 3. Second Pass: Apply Directory Data Updates
            // We apply the record if it matches the OLD block OR the NEW block.
            // This ensures that if the transaction moved the block AND filled it, we get the data.
            for (int i = 0; i < pending_count; i++) {
                struct data_record *dr = pending_recs[i];
                if (dr->block_no == *current_root_data_blk_idx || 
                   (root_moved && dr->block_no == next_root_blk)) {
                    memcpy(root_data_block, dr->data, BLOCK_SIZE);
                }
            }

            // 4. Finally update the tracked index
            if (root_moved) {
                *current_root_data_blk_idx = next_root_blk;
            }

            pending_count = 0; 
        }
        
        offset += rh->size;
    }

    free(journal_mem);
}

// ==========================================
// 4. CMD: CREATE
// ==========================================

void cmd_create(const char *filename) {
    if (strlen(filename) == 0 || strlen(filename) > 27) {
        fprintf(stderr, "Error: Invalid filename length.\n");
        exit(EXIT_FAILURE);
    }
    if (strcmp(filename, ".") == 0 || strcmp(filename, "..") == 0 || strchr(filename, '/')) {
        fprintf(stderr, "Error: Invalid filename content.\n");
        exit(EXIT_FAILURE);
    }

    int fd = open("vsfs.img", O_RDWR);
    if (fd < 0) die("Could not open vsfs.img");

    uint8_t sb_buf[BLOCK_SIZE];
    read_block(fd, 0, sb_buf);
    struct superblock *sb = (struct superblock *)sb_buf;
    
    // FIX #10: Better Superblock validation
    if (sb->magic != FS_MAGIC) die("Invalid superblock magic");
    if (sb->block_size != BLOCK_SIZE) die("Invalid block size");
    if (sb->journal_block != JOURNAL_BLOCK_IDX) die("Invalid journal layout");

    uint8_t inode_bitmap[BLOCK_SIZE];
    uint8_t *inode_table_full = safe_malloc(INODE_BLOCKS_CNT * BLOCK_SIZE); 
    uint8_t root_data_block[BLOCK_SIZE];

    read_block(fd, sb->inode_start, inode_table_full); 
    struct inode *root_node = (struct inode *)inode_table_full;
    uint32_t root_data_blk_idx = root_node->direct[0]; 
    
    if (root_data_blk_idx == 0) die("Corrupt root inode: no data block");
    if (!is_valid_target_block(sb, root_data_blk_idx)) die("Root directory block out of bounds");

    // Load State
    load_current_state(fd, sb, inode_bitmap, inode_table_full, root_data_block, &root_data_blk_idx);
    
    // Refresh pointer
    root_node = (struct inode *)inode_table_full;

    // FIX #3: Normalize Root Inode (Self-healing)
    root_node->type = 2; // Directory
    // Ensure links is at least 2 (for . and ..). We don't increment for new files in this simple FS,
    // but we ensure it's not garbage.
    if (root_node->links < 2) root_node->links = 2;

    int free_inode_idx = -1;
    for (uint32_t i = 1; i < sb->inode_count; i++) {
        if (check_bit(inode_bitmap, i) == 0) {
            free_inode_idx = i;
            break;
        }
    }
    if (free_inode_idx == -1) {
        fprintf(stderr, "Error: No free inodes.\n");
        goto cleanup;
    }

    // FIX #4: Verify Inode Consistency (Bitmap says free, Inode must be type 0)
    uint32_t inodes_per_block = BLOCK_SIZE / INODE_SIZE;
    uint32_t check_inode_blk_offset = free_inode_idx / inodes_per_block;
    uint32_t check_inode_idx_in_blk = free_inode_idx % inodes_per_block;
    struct inode *check_blk_ptr = (struct inode *)(inode_table_full + (check_inode_blk_offset * BLOCK_SIZE));
    struct inode *candidate_node = &check_blk_ptr[check_inode_idx_in_blk];
    
    if (candidate_node->type != 0) {
        fprintf(stderr, "Error: Inconsistency detected. Bitmap says inode %d is free, but type is %d.\n", free_inode_idx, candidate_node->type);
        goto cleanup;
    }

    struct dirent *dirs = (struct dirent *)root_data_block;
    int free_dir_idx = -1;
    int max_entries = BLOCK_SIZE / sizeof(struct dirent);

    for (int i = 0; i < max_entries; i++) {
        // FIX #1: Correct free slot detection
        bool is_free = (dirs[i].inode == 0 && dirs[i].name[0] == '\0');
        
        if (!is_free && is_name_match(dirs[i].name, filename)) {
            fprintf(stderr, "Error: File '%s' already exists.\n", filename);
            goto cleanup;
        }

        if (is_free && free_dir_idx == -1) {
            free_dir_idx = i;
        }
    }

    if (free_dir_idx == -1) {
        fprintf(stderr, "Error: Root directory full.\n");
        goto cleanup;
    }

    // Apply Changes
    time_t now = time(NULL);

    set_bit(inode_bitmap, free_inode_idx);

    struct inode *new_node = candidate_node; // Reusing pointer from check above
    memset(new_node, 0, sizeof(struct inode));
    new_node->type = 1; 
    new_node->links = 1;
    new_node->size = 0;
    new_node->ctime = (uint32_t)now;
    new_node->mtime = (uint32_t)now;

    uint32_t min_size = (free_dir_idx + 1) * sizeof(struct dirent);
    if (root_node->size < min_size) {
        root_node->size = min_size;
    }
    if (root_node->size % sizeof(struct dirent) != 0) {
        root_node->size = ((root_node->size / sizeof(struct dirent)) + 1) * sizeof(struct dirent);
    }
    root_node->mtime = (uint32_t)now;

    dirs[free_dir_idx].inode = free_inode_idx;
    memset(dirs[free_dir_idx].name, 0, 28);
    strncpy(dirs[free_dir_idx].name, filename, 27);

    // Prepare Journal
    bool same_inode_block = (check_inode_blk_offset == 0);
    uint32_t num_inode_blocks = same_inode_block ? 1 : 2;
    uint32_t total_recs = 1 + 1 + num_inode_blocks; 
    uint32_t txn_size = (total_recs * sizeof(struct data_record)) + sizeof(struct commit_record);

    uint8_t *journal_mem = safe_malloc(TOTAL_JOURNAL_SIZE);
    for (int i = 0; i < JOURNAL_BLOCKS; i++) {
        read_block(fd, sb->journal_block + i, journal_mem + (i * BLOCK_SIZE));
    }
    struct journal_header *j_hdr = (struct journal_header *)journal_mem;

    // FIX #2: Reset if nbytes_used is garbage, even if magic matches
    if (j_hdr->magic != JOURNAL_MAGIC || 
        j_hdr->nbytes_used < sizeof(struct journal_header) || 
        j_hdr->nbytes_used > TOTAL_JOURNAL_SIZE) {
        
        j_hdr->magic = JOURNAL_MAGIC;
        j_hdr->nbytes_used = sizeof(struct journal_header);
        memset(journal_mem + sizeof(struct journal_header), 0, TOTAL_JOURNAL_SIZE - sizeof(struct journal_header));
    }

    if (j_hdr->nbytes_used + txn_size > TOTAL_JOURNAL_SIZE) {
        fprintf(stderr, "Error: Journal full. Please run ./journal install\n");
        free(journal_mem); goto cleanup;
    }

    uint8_t *j_ptr = journal_mem + j_hdr->nbytes_used;

    // Helper macro to write record safely (FIX #9 included implicitly by strictly defining blocks)
    #define WRITE_REC(blk, buf) do { \
        if (!is_valid_target_block(sb, blk)) { \
            fprintf(stderr, "Error: Attempting to journal invalid block %u\n", blk); \
            free(journal_mem); goto cleanup; \
        } \
        struct data_record *rec = (struct data_record *)j_ptr; \
        rec->hdr.type = REC_DATA; \
        rec->hdr.size = sizeof(struct data_record); \
        rec->block_no = blk; \
        memcpy(rec->data, buf, BLOCK_SIZE); \
        j_ptr += sizeof(struct data_record); \
    } while(0)

    WRITE_REC(sb->inode_bitmap, inode_bitmap);
    WRITE_REC(root_data_blk_idx, root_data_block);
    WRITE_REC(sb->inode_start, inode_table_full); // Root inode block

    if (!same_inode_block) {
        WRITE_REC(sb->inode_start + check_inode_blk_offset, (inode_table_full + (check_inode_blk_offset * BLOCK_SIZE)));
    }

    struct commit_record *crec = (struct commit_record *)j_ptr;
    crec->hdr.type = REC_COMMIT;
    crec->hdr.size = sizeof(struct commit_record);
    j_ptr += sizeof(struct commit_record);

    j_hdr->nbytes_used += txn_size;

    for (int i = 0; i < JOURNAL_BLOCKS; i++) {
        write_block(fd, sb->journal_block + i, journal_mem + (i * BLOCK_SIZE));
    }

    fsync(fd);
    free(journal_mem);
    printf("Successfully created file '%s' in journal.\n", filename);

cleanup:
    free(inode_table_full);
    close(fd);
    if (free_inode_idx == -1 || free_dir_idx == -1) exit(EXIT_FAILURE);
}

// ==========================================
// 5. CMD: INSTALL
// ==========================================

void cmd_install() {
    int fd = open("vsfs.img", O_RDWR);
    if (fd < 0) die("Could not open vsfs.img");

    uint8_t sb_buf[BLOCK_SIZE];
    read_block(fd, 0, sb_buf);
    struct superblock *sb = (struct superblock *)sb_buf;

    uint8_t *journal_mem = safe_malloc(TOTAL_JOURNAL_SIZE);
    for (int i = 0; i < JOURNAL_BLOCKS; i++) {
        read_block(fd, sb->journal_block + i, journal_mem + (i * BLOCK_SIZE));
    }

    struct journal_header *j_hdr = (struct journal_header *)journal_mem;
    
    if (j_hdr->magic != JOURNAL_MAGIC || 
        j_hdr->nbytes_used < sizeof(struct journal_header) || 
        j_hdr->nbytes_used > TOTAL_JOURNAL_SIZE) {
        printf("Journal empty or invalid. Nothing to install.\n");
        free(journal_mem); close(fd); return;
    }

    uint32_t offset = sizeof(struct journal_header);
    struct data_record *pending_recs[MAX_TXN_RECORDS];
    int pending_count = 0;
    int transactions_installed = 0;

    while (offset < j_hdr->nbytes_used) {
        if (offset + sizeof(struct rec_header) > TOTAL_JOURNAL_SIZE) break;

        struct rec_header *rh = (struct rec_header *)(journal_mem + offset);
        
        if (rh->type == REC_DATA && rh->size != sizeof(struct data_record)) break;
        if (rh->type == REC_COMMIT && rh->size != sizeof(struct commit_record)) break;
        if (rh->size == 0 || offset + rh->size > j_hdr->nbytes_used) break;

        if (rh->type == REC_DATA) {
            struct data_record *dr = (struct data_record *)rh;
            if (is_valid_target_block(sb, dr->block_no)) {
                // FIX #8: Abort on overflow
                if (pending_count >= MAX_TXN_RECORDS) {
                    fprintf(stderr, "Error: Journal corruption (Transaction too large).\n");
                    free(journal_mem); close(fd); exit(EXIT_FAILURE);
                }
                pending_recs[pending_count++] = dr;
            }
        } 
        else if (rh->type == REC_COMMIT) {
            for (int i = 0; i < pending_count; i++) {
                struct data_record *dr = pending_recs[i];
                write_block(fd, dr->block_no, dr->data);
            }
            transactions_installed++;
            pending_count = 0;
        }
        else {
            break;
        }

        offset += rh->size;
    }

    j_hdr->nbytes_used = sizeof(struct journal_header);
    memset(journal_mem + sizeof(struct journal_header), 0, TOTAL_JOURNAL_SIZE - sizeof(struct journal_header));

    for (int i = 0; i < JOURNAL_BLOCKS; i++) {
        write_block(fd, sb->journal_block + i, journal_mem + (i * BLOCK_SIZE));
    }

    fsync(fd);
    free(journal_mem);
    close(fd);
    printf("Installed %d transactions. Journal cleared.\n", transactions_installed);
}

// ==========================================
// 6. MAIN
// ==========================================

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <command> [args]\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    if (strcmp(argv[1], "create") == 0) {
        if (argc != 3) {
            fprintf(stderr, "Usage: %s create <filename>\n", argv[0]);
            exit(EXIT_FAILURE);
        }
        cmd_create(argv[2]);
    } 
    else if (strcmp(argv[1], "install") == 0) {
        cmd_install();
    } 
    else {
        fprintf(stderr, "Unknown command: %s\n", argv[1]);
        exit(EXIT_FAILURE);
    }

    return 0;
}