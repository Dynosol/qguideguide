import { MRT_ColumnDef } from 'material-react-table';
import { Course } from './db';
import { googleSearchFilter } from '../../utils/searchHelper';
import { colorPalettes } from '../../utils/colors';
import { ThemeMode } from '../../utils/themeHelper';
import Tooltip from '@mui/material/Tooltip';

// Helper function to create rating cells
const createRatingCell = (mode: ThemeMode, ratingKey: keyof Course) => ({
  Cell: ({ row }: any) => {
    const {
      [`${ratingKey}`]: rating,
      [`${ratingKey}_bayesian_score`]: bayesianScore,
      [`${ratingKey.replace('rating', 'grade')}`]: grade, 
      [`${ratingKey}_bayesian_score_department`]: deptBayesianScore,
      [`${ratingKey.replace('rating', 'grade')}_department`]: deptGrade, 
    } = row.original;

    if (!rating) {
      return <em>No Data</em>;
    }

    return (
      <div>
        <span>
          <strong>
            {bayesianScore} ({grade})
          </strong>
        </span>
        {' | '}
        <span style={{ color: colorPalettes[mode].harvard }}>
          {deptBayesianScore} (<strong>{deptGrade}</strong>)
        </span>
        {' | '}
        <i>{rating}</i>
      </div>
    );
  },
});

const ratingDefinitions: { key: keyof Course; header: string, minSize: number }[] = [
  { key: 'course_mean_rating', header: 'Course Overall Score', minSize: 250 },
  { key: 'materials_mean_rating', header: 'Course Materials', minSize: 230 },
  { key: 'assignments_mean_rating', header: 'Assignments Quality', minSize: 250 },
  { key: 'feedback_mean_rating', header: 'Feedback Rating', minSize: 250 },
  { key: 'section_mean_rating', header: 'Section Rating', minSize: 200 },
  { key: 'instructor_mean_rating', header: 'Instructor Overall Rating', minSize: 270 },
  { key: 'effective_mean_rating', header: 'Inst. Effectiveness', minSize: 230 },
  { key: 'accessible_mean_rating', header: 'Inst. is Accessible Outside Class', minSize: 330 },
  { key: 'enthusiasm_mean_rating', header: 'Inst. Enthusiasm', minSize: 220 },
  { key: 'discussion_mean_rating', header: 'Inst. Facilitates Discussion', minSize: 290 },
  { key: 'inst_feedback_mean_rating', header: 'Inst. Feedback Usefulness', minSize: 280 },
  { key: 'returns_mean_rating', header: 'Inst. Timely Assignment Returns', minSize: 330 },
];


export const getCoursesColumns = (
  mode: ThemeMode,
  position: string,
  departments: string[],
  terms: string[],
  ): MRT_ColumnDef<Course>[] => {
  // THIS IS FROM THE DROPDOWN AND MODIFIES WHAT THE COLUMNS ARE FILTERED BY
  const getAccessorSuffix = (position: string) => {
    switch (position) {
      case "weighted":
        return "_bayesian_score";
      case "weighted-department":
        return "_bayesian_score_department";
      case "naive":
        return ""; // Assuming this refers to the raw rating
      default:
        return "_bayesian_score"; // Fallback
    }
  };
  


  // Base columns that are not ratings
  const baseColumns: MRT_ColumnDef<Course>[] = [
    {
      accessorKey: 'title',
      header: 'Course Title',
      filterFn: googleSearchFilter,
      minSize: 400,
    },
    {
      accessorKey: 'department',
      header: 'Department',
      filterVariant: 'multi-select',
      filterSelectOptions: departments,
      filterFn: (row, id, filterValue: string[]) => {
        if (!filterValue?.length) return true;
        const rowValue = row.getValue<string>(id);
        return filterValue.some((value) => rowValue === value);
      }
    },
    {
      accessorKey: 'instructor',
      header: 'Instructor',
      filterFn: googleSearchFilter,
      minSize: 150,
    },
    {
      accessorKey: 'term',
      header: 'Term',
      minSize: 100,
      filterSelectOptions: terms,
      filterVariant: 'multi-select',
      filterFn: (row, id, filterValue: string[]) => {
        if (!filterValue?.length) return true;
        const rowValue = row.getValue<string>(id);
        return filterValue.some((value) => rowValue === value);
      }
    },
    {
      accessorKey: 'blue_course_id',
      header: 'Blue Course ID',
      filterFn: googleSearchFilter,
      minSize: 200,
    },
    {
      accessorKey: 'responses',
      header: 'Responses',
      minSize: 200,
    },
    {
      accessorKey: 'invited_responses',
      header: 'Size',
      filterVariant: 'range',
      minSize: 150,
    },
    {
      accessorKey: 'response_ratio',
      header: 'Response Rate',
      Cell: ({ cell }: any) => `${(cell.getValue() as number * 100).toFixed(0)}%`,
      minSize: 250,
      filterVariant: 'range-slider',
      muiFilterSliderProps: {
        max: 1,
        min: 0,
        step: 0.01,
        valueLabelFormat: (value: number) => `${(value * 100).toFixed(0)}%`,
      },
    },
  ];

  // Dynamically generate rating columns
  const ratingColumns: MRT_ColumnDef<Course>[] = ratingDefinitions.map((rating) => ({
    accessorKey: `${rating.key}${getAccessorSuffix(position)}`,
    header: rating.header,
    filterVariant: 'range-slider',
    muiFilterSliderProps: {
      max: 5,
      min: 0,
      step: 0.05,
    },
    minSize: rating.minSize,
    ...createRatingCell(mode, rating.key),
  }));

  const additionalColumns: MRT_ColumnDef<Course>[] = [
    {
      accessorKey: 'hours_mean_rating',
      header: 'Mean Hours',
      filterVariant: 'range-slider',
      muiFilterSliderProps: {
        step: 0.1,
      },
      Cell: ({ cell }: any) => (
        <Tooltip title="Mean Hours" placement="top">
          <i>{cell.getValue() || 'No Data'}</i>

          {/* <img src={hoursExampleImage}/> */}
        </Tooltip>
      ),
    },
    {
      accessorKey: 'recommend_mean_rating',
      header: 'Mean Recommendation',
      minSize: 250,
      filterVariant: 'range-slider',
      muiFilterSliderProps: {
        max: 5,
        min: 0,
        step: 0.1,
      },
      Cell: ({ cell }: any) => <i>{cell.getValue() || 'No Data'}</i>,
    },
    {
      accessorKey: 'number_comments',
      header: 'Number of Comments',
      minSize: 250,
      filterVariant: 'range',
      Cell: ({ cell }: any) => <i>{cell.getValue() || 'No Data'}</i>,
    },
    {
      accessorKey: 'url',
      header: 'QGuide Link',
      minSize: 200,
      Cell: ({ cell }: any) => {
        const url = cell.getValue() as string;
        return (
          <a href={url} target="_blank" rel="noreferrer" className="guide-link">
            QGuide Link
          </a>
        );
      },
    },
  ];

  // Combine all columns
  const columns = [
    ...baseColumns,
    ...ratingColumns,
    ...additionalColumns,
  ];

  return columns;
};
