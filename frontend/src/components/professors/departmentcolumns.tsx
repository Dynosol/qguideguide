import { ColumnDef } from '@tanstack/react-table';
import { Department } from './db';
import { colorPalettes } from '../../utils/colors';

const getOrdinalSuffix = (rank: number): string => {
  const lastDigit = rank % 10;
  const lastTwoDigits = rank % 100;
  
  if (lastTwoDigits >= 11 && lastTwoDigits <= 13) {
    return rank + 'th';
  }
  
  switch (lastDigit) {
    case 1: return rank + 'st';
    case 2: return rank + 'nd';
    case 3: return rank + 'rd';
    default: return rank + 'th';
  }
};

export const getDepartmentsColumns = (mode: 'light' | 'dark'): ColumnDef<Department>[] => [
  {
    accessorKey: 'name',
    header: 'Department',
  },
  {
    accessorKey: 'empirical_bayes_average',
    header: 'Average Score',
    cell: ({ row, getValue }) => (
      <strong>
        <span style={{ color: colorPalettes[mode].harvard}}> 
          {getValue<number>()?.toFixed(3)} 
        </span>
        <span>
          &nbsp; (Avg. Rank: {getOrdinalSuffix(Math.round(row.original.empirical_bayes_rank))})
        </span>
      </strong>
    ),
  }
];
