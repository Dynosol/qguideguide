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
import axios from 'axios';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { getDepartmentsColumns } from './departmentcolumns';
import { Department, db } from './db';
import { useThemeContext } from '../../utils/themeHelper';

export const DepartmentsTable: React.FC = () => {
  const [sorting, setSorting] = React.useState<SortingState>([]);
  const [columnVisibility, setColumnVisibility] = React.useState<VisibilityState>({});
  const [data, setData] = React.useState<Department[]>([]);
  const [isLoading, setIsLoading] = React.useState(true);
  const { mode } = useThemeContext();

  // Load data on mount
  React.useEffect(() => {
    (async () => {
      try {
        // Try to load from IndexedDB first
        const localData = await db.departments.toArray();
        if (localData.length > 0) {
          setData(localData);
          setIsLoading(false);
        } else {
          // If no local data, fetch from API
          await fetchAndStoreDepartments();
        }
      } catch (error) {
        console.error('Error loading from Dexie', error);
        setIsLoading(false);
      }
    })();
  }, []);

  const fetchAndStoreDepartments = async () => {
    setIsLoading(true);
    try {
      const response = await axios.get<{ results: Department[] }>('http://localhost:8000/api/professors/departments/');
      console.log(response.data);
      const departments: Department[] = response.data.results;

      await db.departments.clear();
      await db.departments.bulkAdd(departments);
      console.log('Departments successfully stored in IndexedDB');

      setData(departments);
    } catch (error) {
      console.error('Error fetching or storing departments:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const columns = React.useMemo<ColumnDef<Department>[]>(
    () => getDepartmentsColumns(mode),
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
    return <div>Loading...</div>;
  }

  return (
    <div className="w-full h-full flex flex-col">
      {/* Title */}
      <h2 className="text-2xl font-semibold mb-4 text-gray-800">
        Department Averages
      </h2>

      {/* Table Container */}
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
