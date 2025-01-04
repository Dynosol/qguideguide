import React, { useState } from 'react';
import axios from 'axios';
import {
  Table,
  TableHeader,
  TableRow,
  TableHead,
  TableBody,
  TableCell,
} from "@/components/ui/table";
import {
  ColumnDef,
  flexRender,
  getCoreRowModel,
  getSortedRowModel,
  SortingState,
  useReactTable,
} from "@tanstack/react-table";
import { db, Department } from './db';
import { useThemeContext } from '../../utils/themeHelper';
import { getDepartmentsColumns } from './departmentcolumns';

export function DepartmentsTable() {
  const [data, setData] = useState<Department[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [sorting, setSorting] = useState<SortingState>([]);
  const [columnVisibility, setColumnVisibility] = useState({});

  const { mode } = useThemeContext();

  // Load data on mount
  React.useEffect(() => {
    (async () => {
      try {
        // First check if we have any local data
        const localData = await db.departments.toArray();
        const lastUpdateTime = await db.metadata.get('lastUpdate');

        if (localData.length > 0 && lastUpdateTime) {
          // Check with the server if data has been updated
          const response = await axios.head('http://localhost:8000/api/professors/departments/');
          const serverLastModified = response.headers['last-modified'];

          if (serverLastModified && new Date(serverLastModified) <= new Date(lastUpdateTime.value)) {
            // Use cached data if server hasn't updated
            setData(localData);
            setIsLoading(false);
            return;
          }
        }

        // If we reach here, we need to fetch new data
        await fetchAndStoreDepartments();
      } catch (error) {
        console.error('Error loading from Dexie', error);
        setIsLoading(false);
      }
    })();
  }, []);

  const fetchAndStoreDepartments = async () => {
    setIsLoading(true);
    try {
      const response = await axios.get<Department[]>('http://localhost:8000/api/professors/departments/');
      const departments: Department[] = response.data;

      // Store the current timestamp
      const currentTime = new Date().toISOString();

      await db.transaction('rw', db.departments, db.metadata, async () => {
        await db.departments.clear();
        await db.departments.bulkAdd(departments);
        await db.metadata.put({ key: 'lastUpdate', value: currentTime });
      });

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
        Department Scores (Overall)
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
            {table.getRowModel().rows?.length ? (
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
}
