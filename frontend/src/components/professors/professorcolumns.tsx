import { ColumnDef } from '@tanstack/react-table';
import { Professor } from './db';
import { colorPalettes } from '../../utils/colors';
// import { googleSearchFilter } from '@/utils/searchHelper';
import { ArrowUpDown } from "lucide-react"
import { Button } from "@/components/ui/button"


const getOrdinalSuffix = (rank: number | string): string => {
  // Convert to number if string and log the input type
  console.log('Rank input type:', typeof rank, 'Value:', rank);
  
  const rankNum = typeof rank === 'string' ? parseFloat(rank) : rank;
  
  // Ensure we have a valid number
  if (typeof rankNum !== 'number' || isNaN(rankNum)) {
    console.warn('Invalid rank provided to getOrdinalSuffix:', rank);
    return 'N/A';
  }

  // Ensure we're working with a positive integer
  const finalRank = Math.abs(Math.round(rankNum));
  
  const lastDigit = finalRank % 10;
  const lastTwoDigits = finalRank % 100;
  
  if (lastTwoDigits >= 11 && lastTwoDigits <= 13) {
    return finalRank + 'th';
  }
  
  switch (lastDigit) {
    case 1: return finalRank + 'st';
    case 2: return finalRank + 'nd';
    case 3: return finalRank + 'rd';
    default: return finalRank + 'th';
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
    minSize: 50,
    maxSize: 100,
  },
  {
    accessorKey: 'empirical_bayes_average',
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
        >
          Rating
          <ArrowUpDown className="ml-2" />
        </Button>
      )
    },
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
  {
    accessorKey: 'intra_department_eb_average',
    header: 'Department Score',
    size: 160,
    cell: ({ row, getValue }) => {
      // Add debug logging for intra_department_ranks
      console.log('Intra department ranks:', {
        value: row.original.intra_department_ranks,
        type: typeof row.original.intra_department_ranks,
        row: row.original
      });
      
      return (
        <strong>
          <span style={{ color: colorPalettes[mode].harvard }}>
            <strong>{getValue<number>()?.toFixed(3)}</strong>
          </span>
          <span>
              &nbsp; ({row.original.intra_department_letter_grade}) ({(row.original.intra_department_ranks)})
          </span>
        </strong>
      );
    },
  },
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
