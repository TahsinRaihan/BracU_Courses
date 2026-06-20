
# Metadata Journaling File System Layer

This is a C implementation of a crash-consistent metadata journaling layer for a VSFS-like file system. The program interacts directly with a raw disk image (`vsfs.img`) to log structural updates to a dedicated journal before safely applying them to their actual home blocks.

## File System Layout
The file system has a static **4 KB block size** across a total of **85 blocks**:

* **Superblock (1 block)**: Stores file system configuration and block layout.
* **Journal (16 blocks)**: Append-only space that logs transactions.
* **Inode Bitmap (1 block)**: Tracks which inodes are free or allocated.
* **Data Bitmap (1 block)**: Tracks allocated data blocks.
* **Inode Table (2 blocks)**: Holds raw 128-byte inode structures.
* **Data Blocks (64 blocks)**: Stores directory entries and file data.

---

## How it Works

### 1. Creating a File (`./journal create <name>`)
When you run the create command, the tool computes what changes need to happen but **does not** modify the actual metadata blocks in their home locations. Instead, it:
* Finds a free inode slot in the bitmap.
* Allocates a free slot in the root directory data block.
* Logs the entire updated block images to the journal as `DATA` records.
* Appends a `COMMIT` record to mark the transaction as valid and complete.

### 2. Installing Transactions (`./journal install`)
To apply the changes permanently, the install command safely replays the logged transactions:
* It reads the 16 journal blocks sequentially.
* For every transaction finalized with a valid `COMMIT` record, it updates the absolute home block numbers on disk with the logged `DATA` records.
* Once all committed records are replayed, it clears the journal header back to empty.

---

## Technical Specifications

### Journal Header Layout
```c
struct journal_header {
    uint32_t magic;         // JOURNAL_MAGIC (0x4A524E4C)
    uint32_t nbytes_used;   // Tracks where the next append offset is
};

```

### Record Structure

Every entry inside the journal uses a simple record header to track the type (`REC_DATA` or `REC_COMMIT`) and total size.

* **DATA Record**: Contains the absolute target block number and the full 4096-byte content.
* **COMMIT Record**: Acts as a barrier ensuring all preceding data blocks are safe to recover.

---

## Compilation & Usage

### 1. Compile the code

```bash
gcc -Wall -Wextra -O2 journal.c -o journal

```

### 2. Initialize the file system image

If you have the `mkfs` companion tool available, run it to reset or create a clean disk image:

```bash
./mkfs

```

### 3. Run Commands

* **Log a file creation entry into the journal:**
```bash
./journal create sample.txt

```


* **Install and checkpoint all committed transactions to disk:**
```bash
./journal install

```



### 4. Run the Validator

To verify that everything is structurally intact and completely consistent, run the validator binary:

```bash
./validator

```

```

```