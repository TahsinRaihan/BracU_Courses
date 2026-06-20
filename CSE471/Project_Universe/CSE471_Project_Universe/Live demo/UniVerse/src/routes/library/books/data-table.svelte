<script lang="ts" generics="TData, TValue">
  import {
    type ColumnDef,
    type PaginationState,
    type SortingState,
    type ColumnFiltersState,
    getCoreRowModel,
    getPaginationRowModel,
    getSortedRowModel,
    getFilteredRowModel,
  } from "@tanstack/table-core";
  import {
    createSvelteTable,
    FlexRender,
  } from "$lib/components/ui/data-table/index.js";
  import * as Table from "$lib/components/ui/table/index.js";
  import { Input } from "$lib/components/ui/input/index.js";

  type DataTableProps<TData, TValue> = {
    columns: ColumnDef<TData, TValue>[];
    data: TData[];
  };

  let { data: originalData, columns }: DataTableProps<TData, TValue> = $props();
  let searchValue = $state("");
  
  // Reactive filtered data
  let filteredData = $derived.by(() => {
    // First filter out books with no meaningful copies
    const booksWithMeaningfulCopies = originalData.filter((row: any) => {
      const availableCopies = row.availableCopies || 0;
      const borrowedCopies = row.borrowedCopies || 0;
      const reservedCopies = row.reservedCopies || 0;
      return availableCopies > 0 || borrowedCopies > 0 || reservedCopies > 0;
    });
    
    if (!searchValue) return booksWithMeaningfulCopies;
    
    const searchLower = searchValue.toLowerCase();
    return booksWithMeaningfulCopies.filter((row: any) => {
      const title = (row.title as string).toLowerCase();
      const author = (row.author as string).toLowerCase();
      return title.includes(searchLower) || author.includes(searchLower);
    });
  });

  let pagination = $state<PaginationState>({ pageIndex: 0, pageSize: 10 });
  let sorting = $state<SortingState>([]);
  let columnFilters = $state<ColumnFiltersState>([]);

  const table = createSvelteTable({
    get data() {
      return filteredData;
    },
    columns,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    onPaginationChange: (updater) => {
      if (typeof updater === "function") {
        pagination = updater(pagination);
      } else {
        pagination = updater;
      }
    },
    onSortingChange: (updater) => {
      if (typeof updater === "function") {
        sorting = updater(sorting);
      } else {
        sorting = updater;
      }
    },
    onColumnFiltersChange: (updater) => {
      if (typeof updater === "function") {
        columnFilters = updater(columnFilters);
      } else {
        columnFilters = updater;
      }
    },
    state: {
      get pagination() {
        return pagination;
      },
      get sorting() {
        return sorting;
      },
      get columnFilters() {
        return columnFilters;
      },
    },
  });
</script>

<div>
  <div class="flex items-center py-4">
    <Input
      placeholder="Search books by title or author..."
      value={searchValue}
      onchange={(e) => searchValue = e.currentTarget.value}
      oninput={(e) => searchValue = e.currentTarget.value}
      class="max-w-sm"
    />
  </div>
  <div class="rounded-md border">
    <Table.Root>
      <Table.Header>
        {#each table.getHeaderGroups() as headerGroup (headerGroup.id)}
          <Table.Row>
            {#each headerGroup.headers as header (header.id)}
              <Table.Head colspan={header.colSpan} class={header.column.id === 'image_url' ? 'w-20' : ''}>
                {#if !header.isPlaceholder}
                  <FlexRender
                    content={header.column.columnDef.header}
                    context={header.getContext()}
                  />
                {/if}
              </Table.Head>
            {/each}
          </Table.Row>
        {/each}
      </Table.Header>
      <Table.Body>
        {#each table.getRowModel().rows as row (row.id)}
          <Table.Row data-state={row.getIsSelected() && "selected"}>
            {#each row.getVisibleCells() as cell (cell.id)}
              <Table.Cell class={cell.column.id === 'image_url' ? 'w-20' : ''}>
                {#if cell.column.id === 'image_url'}
                  {@const imageUrl = row.getValue('image_url')}
                  {@const title = row.getValue('title')}
                  {#if imageUrl}
                    <img 
                      src={imageUrl} 
                      alt="Cover of {title}" 
                      class="w-16 h-20 object-cover rounded border shadow-sm"
                    />
                  {:else}
                    <div class="w-16 h-20 bg-gray-100 rounded border flex items-center justify-center text-gray-400 text-2xl">
                      📚
                    </div>
                  {/if}
                {:else}
                  <FlexRender
                    content={cell.column.columnDef.cell}
                    context={cell.getContext()}
                  />
                {/if}
              </Table.Cell>
            {/each}
          </Table.Row>
        {:else}
          <Table.Row>
            <Table.Cell colspan={columns.length} class="h-24 text-center">
              No books found.
            </Table.Cell>
          </Table.Row>
        {/each}
      </Table.Body>
    </Table.Root>
  </div>
</div>
