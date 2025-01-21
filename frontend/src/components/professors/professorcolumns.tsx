import { ColumnDef } from '@tanstack/react-table';
import { Professor } from './db';
import { colorPalettes } from '../../utils/colors';
// import { googleSearchFilter } from '@/utils/searchHelper';
import { ArrowUpDown } from "lucide-react"
import { Button } from "@/components/ui/button"


const getOrdinalSuffix = (rank: number | string): string => {
  // Convert to number if string and log the input type
  // console.log('Rank input type:', typeof rank, 'Value:', rank);
  
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

const parseDepartmentMetrics = (metrics: string): { dept: string, avg: number, grade: string, rank: string } | null => {
  if (!metrics) return null;
  
  try {
    // Handle both old and new formats
    // Old format: "COMPLIT: 4 (B-, Rank: 15)"
    // New format: "COMPLIT: 4"
    const [dept, rest] = metrics.split(': ');
    
    if (rest.includes('(')) {
      // New format with grade and rank
      const match = rest.match(/(\d+\.\d+)\s*\(([A-Z][+-]?),\s*Rank:\s*(\d+)\)/);
      if (match) {
        return {
          dept: dept.trim(),
          avg: parseFloat(match[1]),
          grade: match[2],
          rank: match[3]
        };
      }
    } else {
      // Old format with just the average
      return {
        dept: dept.trim(),
        avg: parseFloat(rest),
        grade: '',
        rank: ''
      };
    }
  } catch (error) {
    console.error('Error parsing department metrics:', error);
  }
  return null;
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
    accessorKey: 'department_metrics',
    header: 'Department Metrics',
    size: 160,
    cell: ({ row }) => {
      const metrics = row.getValue('department_metrics') as string | undefined;
      if (!metrics) return null;

      // Handle multiple departments (split by |)
      const departmentMetrics = metrics.split(' | ').map((metric: string) => {
        const parsed = parseDepartmentMetrics(metric);
        if (parsed) {
          return `${parsed.dept}: ${parsed.avg.toFixed(3)} (${parsed.grade}, ${getOrdinalSuffix(parsed.rank)})`;
        }
        return null;
      }).filter(Boolean);

      return (
        <div>
          {departmentMetrics.map((metric, index) => (
            <div key={index}>
              <strong>
                <span style={{ color: colorPalettes[mode].harvard }}>
                  {metric}
                </span>
              </strong>
            </div>
          ))}
        </div>
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
