import { ColumnDef } from '@tanstack/react-table';
import { Professor } from './db';
import { colorPalettes } from '../../utils/colors';
// import { googleSearchFilter } from '@/utils/searchHelper';

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

export const getProfessorsColumns = (mode: 'light' | 'dark'): ColumnDef<Professor>[] => [
  {
    accessorKey: 'name',
    header: 'Name',
  },
  {
    accessorKey: 'departments',
    header: 'Departments',
  },
  {
    accessorKey: 'total_ratings',
    header: 'Total Ratings',
  },
  {
    accessorKey: 'empirical_bayes_average',
    header: 'Overall Score',
    cell: ({ row, getValue }) => (
      <strong>
        <span style={{ color: colorPalettes[mode].harvard}}> 
          {getValue<number>()?.toFixed(3)} 
        </span> 
        <span>
            &nbsp; ({row.original.overall_letter_grade}) ({getOrdinalSuffix(row.original.empirical_bayes_rank)})
        </span>
      </strong>
    ),
  },
//   {
//     accessorKey: 'intra_department_eb_average',
//     header: 'Department Score',
//     size: 160,
//     cell: ({ getValue }) => (
//       <span style={{ color: colorPalettes[mode].harvard }}>
//         <strong>{getValue<number>()?.toFixed(2)}</strong>
//       </span>
//     ),
//   },
//   {
//     accessorKey: 'intra_department_letter_grade',
//     header: 'Department Grade',
//     size: 140,
//   },
//   {
//     accessorKey: 'intra_department_ranks',
//     header: 'Department Ranks',
//     size: 140,
//   },
];
