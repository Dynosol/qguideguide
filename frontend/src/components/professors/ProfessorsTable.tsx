  // ProfessorsTable.tsx

  import React from 'react';
  import {
    ColumnDef,
    SortingState,
    VisibilityState,
    flexRender,
    getCoreRowModel,
    getSortedRowModel,
    useReactTable,
  } from "@tanstack/react-table";
  import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
  } from "@/components/ui/table";
  import { getProfessorsColumns } from './professorcolumns';
  import { Professor } from './db';
  import { useThemeContext } from '../../utils/themeHelper';

  interface ProfessorsTableProps {
    data: Professor[];
    isLoading: boolean;
  }

  const SkeletonRow = () => (
    <TableRow>
      {Array.from({ length: 5 }).map((_, index) => (
        <TableCell key={index}>
          <div className="h-4 w-full animate-pulse rounded bg-gray-200 dark:bg-gray-700" />
        </TableCell>
      ))}
    </TableRow>
  );

  export const ProfessorsTable: React.FC<ProfessorsTableProps> = ({ data, isLoading }) => {
    const [sorting, setSorting] = React.useState<SortingState>([]);
    const [columnVisibility, setColumnVisibility] = React.useState<VisibilityState>({});
    const { mode } = useThemeContext();

    const columns = React.useMemo<ColumnDef<Professor>[]>(
      () => getProfessorsColumns(mode),
      [mode]
    );

    const table = useReactTable({
      data,
      columns,
      onSortingChange: setSorting,
      getCoreRowModel: getCoreRowModel(),
      getSortedRowModel: getSortedRowModel(),
      onColumnVisibilityChange: setColumnVisibility,
      state: {
        sorting,
        columnVisibility,
      },
      enableGlobalFilter: true,
    });

    if (isLoading) {
      return (
        <div className="w-full h-full flex flex-col">
          <h2 className="text-2xl font-semibold mb-4 text-gray-800">
            Professor Scores (Overall)
          </h2>
          <div className="rounded-md border flex-1 overflow-y-auto">
            <Table className="w-full table-fixed">
              <TableHeader>
                {table.getHeaderGroups().map((headerGroup) => (
                  <TableRow key={headerGroup.id}>
                    {headerGroup.headers.map((header) => (
                      <TableHead key={header.id} className="truncate">
                        {header.isPlaceholder
                          ? null
                          : flexRender(
                              header.column.columnDef.header,
                              header.getContext()
                            )}
                      </TableHead>
                    ))}
                  </TableRow>
                ))}
              </TableHeader>
              <TableBody>
                {Array.from({ length: 30 }).map((_, index) => (
                  <SkeletonRow key={index} />
                ))}
              </TableBody>
            </Table>
          </div>
        </div>
      );
    }

    return (
      <div className="w-full h-full flex flex-col">
        <h2 className="text-2xl font-semibold mb-4 text-gray-800">
          Professor Scores (Overall)
        </h2>

        <div className="rounded-md border flex-1 overflow-y-auto">
          <Table className="w-full table-fixed">
            <TableHeader>
              {table.getHeaderGroups().map((headerGroup) => (
                <TableRow key={headerGroup.id}>
                  {headerGroup.headers.map((header) => (
                    <TableHead key={header.id} className="truncate">
                      {header.isPlaceholder
                        ? null
                        : flexRender(
                            header.column.columnDef.header,
                            header.getContext()
                          )}
                    </TableHead>
                  ))}
                </TableRow>
              ))}
            </TableHeader>
            <TableBody>
              {table.getRowModel().rows.length > 0 ? (
                table.getRowModel().rows.map((row) => (
                  <TableRow
                    key={row.id}
                    data-state={row.getIsSelected() && "selected"}
                  >
                    {row.getVisibleCells().map((cell) => (
                      <TableCell key={cell.id}>
                        {flexRender(
                          cell.column.columnDef.cell,
                          cell.getContext()
                        )}
                      </TableCell>
                    ))}
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell
                    colSpan={columns.length}
                    className="h-24 text-center"
                  >
                    No results.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </div>
      </div>
    );
  };
