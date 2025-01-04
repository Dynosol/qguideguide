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
import axios from 'axios';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { getProfessorsColumns } from './professorcolumns';
import { Professor, db } from './db';
import { useThemeContext } from '../../utils/themeHelper';

export const ProfessorsTable: React.FC = () => {
  const [sorting, setSorting] = React.useState<SortingState>([]);
  const [columnVisibility, setColumnVisibility] = React.useState<VisibilityState>({});
  const [data, setData] = React.useState<Professor[]>([]);
  const [isLoading, setIsLoading] = React.useState(true);
  const { mode } = useThemeContext();

  // Load data on mount
  React.useEffect(() => {
    (async () => {
      try {
        // First check if we have any local data
        const localData = await db.professors.toArray();
        const lastUpdateTime = await db.metadata.get('lastUpdate');

        if (localData.length > 0 && lastUpdateTime) {
          // Check with the server if data has been updated
          const response = await axios.head('http://localhost:8000/api/professors/professors/');
          const serverLastModified = response.headers['last-modified'];

          if (serverLastModified && new Date(serverLastModified) <= new Date(lastUpdateTime.value)) {
            // Use cached data if server hasn't updated
            setData(localData);
            setIsLoading(false);
            return;
          }
        }

        // If we reach here, we need to fetch new data
        await fetchAndStoreProfessors();
      } catch (error) {
        console.error('Error loading from Dexie', error);
        setIsLoading(false);
      }
    })();
  }, []);

  const fetchAndStoreProfessors = async () => {
    setIsLoading(true);
    try {
      const response = await axios.get<Professor[]>('http://localhost:8000/api/professors/professors/');
      const professors: Professor[] = response.data;

      // Store the current timestamp
      const currentTime = new Date().toISOString();

      await db.transaction('rw', db.professors, db.metadata, async () => {
        await db.professors.clear();
        await db.professors.bulkAdd(professors);
        await db.metadata.put({ key: 'lastUpdate', value: currentTime });
      });

      console.log('Professors successfully stored in IndexedDB');
      setData(professors);
    } catch (error) {
      console.error('Error fetching or storing professors:', error);
    } finally {
      setIsLoading(false);
    }
  };

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
    return <div>Loading...</div>;
  }

  return (
    <div className="w-full h-full flex flex-col">
      {/* Title */}
      <h2 className="text-2xl font-semibold mb-4 text-gray-800">
        Professor Scores (Overall)
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
