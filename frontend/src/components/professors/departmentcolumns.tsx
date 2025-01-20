import { ColumnDef } from '@tanstack/react-table';
import { Department } from './db';
import { colorPalettes } from '../../utils/colors';
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

export const getDepartmentsColumns = (mode: 'light' | 'dark'): ColumnDef<Department>[] => [
  {
    accessorKey: 'name',
    header: 'Department',
  },
  {
    accessorKey: 'empirical_bayes_average',
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
        >
          Average Score
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
          &nbsp; (Avg. Rank: {getOrdinalSuffix(Math.round(row.original.empirical_bayes_rank))})
        </span>
      </strong>
    ),
  }
];
