// departmentcolumns.tsx

import { ColumnDef } from '@tanstack/react-table';
import { Department } from './db';
import { colorPalettes } from '../../utils/colors';

// Utility function to format numbers to two decimal places
const formatNumber = (value: number): string => {
  return value.toFixed(2);
};

// Exported function to get department columns based on the current theme mode
export const getDepartmentsColumns = (mode: 'light' | 'dark'): ColumnDef<Department>[] => [
  {
    accessorKey: 'name',
    header: 'Name',
    cell: ({ getValue }) => getValue<string>(),
  },
  {
    accessorKey: 'mean_empirical_bayes_average',
    header: 'Mean EB Average',
    cell: ({ getValue }) => (
      <span style={{ color: colorPalettes[mode].harvard }}>
        {formatNumber(getValue<number>())}
      </span>
    ),
  },
  {
    accessorKey: 'mean_empirical_bayes_rank',
    header: 'Mean EB Rank',
    cell: ({ getValue }) => (
      <span>
        {formatNumber(getValue<number>())}
      </span>
    ),
  },
];
