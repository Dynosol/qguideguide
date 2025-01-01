import { MRT_ColumnDef } from 'material-react-table';
import { Course } from './db';
import { googleSearchFilter } from '../../utils/searchHelper';
import { colorPalettes } from '../../utils/colors';
import { ThemeMode } from '../../utils/themeHelper';

// Helper function to create rating cells
const createRatingCell = (mode: ThemeMode, ratingKey: keyof Course) => ({
  Cell: ({ row }: any) => {
    const {
      [`${ratingKey}`]: rating,
      [`${ratingKey}_bayesian_score`]: bayesianScore,
      [`${ratingKey.replace('rating', 'grade')}`]: grade, // Correct mapping for grade
      [`${ratingKey}_bayesian_score_department`]: deptBayesianScore,
      [`${ratingKey.replace('rating', 'grade')}_department`]: deptGrade, // Correct mapping for department grade
    } = row.original;

    if (!rating) {
      return <em>No Data</em>;
    }

    return (
      <div>
        <span style={{ color: colorPalettes[mode].harvard }}>
          <strong>
            {bayesianScore} ({grade})
          </strong>
        </span>
        {' | '}
        <span>
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


export const getCoursesColumns = (mode: ThemeMode): MRT_ColumnDef<Course>[] => {
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
      filterFn: (row, id, filterValue: string[]) => {
        if (!filterValue?.length) return true;
        const rowValue = row.getValue<string>(id);
        return filterValue.some((value) => rowValue === value);
      },
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
      filterFn: googleSearchFilter,
      minSize: 100,
      filterVariant: 'multi-select',
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
    accessorKey: `${rating.key}_bayesian_score`,
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
      Cell: ({ cell }: any) => <i>{cell.getValue() || 'No Data'}</i>,
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
          <a href={url} target="_blank" rel="noreferrer">
            <i>QGuide Link</i>
          </a>
        );
      },
    },
  ];

  // Combine all columns
  return [...baseColumns, ...ratingColumns, ...additionalColumns];
};
