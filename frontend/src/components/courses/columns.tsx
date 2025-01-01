// src/components/CoursesTable/coursesColumns.tsx
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

export const getCoursesColumns = (mode: ThemeMode): MRT_ColumnDef<Course>[] => [
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
  // Rating Columns
  {
    accessorKey: 'course_mean_rating_bayesian_score',
    header: 'Course Score',
    filterVariant: 'range-slider',
    muiFilterSliderProps: {
      max: 5,
      min: 0,
      step: 0.05,
    },
    minSize: 220,
    ...createRatingCell(mode, 'course_mean_rating'),
  },
  {
    accessorKey: 'materials_mean_rating_bayesian_score',
    header: 'Materials Rating',
    filterVariant: 'range-slider',
    muiFilterSliderProps: {
      max: 5,
      min: 0,
      step: 0.05,
    },
    minSize: 220,
    ...createRatingCell(mode, 'materials_mean_rating'),
  },
  {
    accessorKey: 'assignments_mean_rating_bayesian_score',
    header: 'Assignments Rating',
    filterVariant: 'range-slider',
    muiFilterSliderProps: {
      max: 5,
      min: 0,
      step: 0.05,
    },
    minSize: 220,
    ...createRatingCell(mode, 'assignments_mean_rating'),
  },
  {
    accessorKey: 'feedback_mean_rating_bayesian_score',
    header: 'Feedback Rating',
    filterVariant: 'range-slider',
    muiFilterSliderProps: {
      max: 5,
      min: 0,
      step: 0.05,
    },
    minSize: 220,
    ...createRatingCell(mode, 'feedback_mean_rating'),
  },
  {
    accessorKey: 'section_mean_rating_bayesian_score',
    header: 'Section Rating',
    filterVariant: 'range-slider',
    muiFilterSliderProps: {
      max: 5,
      min: 0,
      step: 0.05,
    },
    minSize: 220,
    ...createRatingCell(mode, 'section_mean_rating'),
  },
  {
    accessorKey: 'instructor_mean_rating_bayesian_score',
    header: 'Instructor Rating',
    filterVariant: 'range-slider',
    muiFilterSliderProps: {
      max: 5,
      min: 0,
      step: 0.05,
    },
    minSize: 220,
    ...createRatingCell(mode, 'instructor_mean_rating'),
  },
  {
    accessorKey: 'effective_mean_rating_bayesian_score',
    header: 'Effective Rating',
    filterVariant: 'range-slider',
    muiFilterSliderProps: {
      max: 5,
      min: 0,
      step: 0.05,
    },
    minSize: 220,
    ...createRatingCell(mode, 'effective_mean_rating'),
  },
  {
    accessorKey: 'accessible_mean_rating_bayesian_score',
    header: 'Accessible Rating',
    filterVariant: 'range-slider',
    muiFilterSliderProps: {
      max: 5,
      min: 0,
      step: 0.05,
    },
    minSize: 220,
    ...createRatingCell(mode, 'accessible_mean_rating'),
  },
  {
    accessorKey: 'enthusiasm_mean_rating_bayesian_score',
    header: 'Enthusiasm Rating',
    filterVariant: 'range-slider',
    muiFilterSliderProps: {
      max: 5,
      min: 0,
      step: 0.05,
    },
    minSize: 220,
    ...createRatingCell(mode, 'enthusiasm_mean_rating'),
  },
  {
    accessorKey: 'discussion_mean_rating_bayesian_score',
    header: 'Discussion Rating',
    filterVariant: 'range-slider',
    muiFilterSliderProps: {
      max: 5,
      min: 0,
      step: 0.05,
    },
    minSize: 220,
    ...createRatingCell(mode, 'discussion_mean_rating'),
  },
  {
    accessorKey: 'inst_feedback_mean_rating_bayesian_score',
    header: 'Instructor Feedback Rating',
    filterVariant: 'range-slider',
    muiFilterSliderProps: {
      max: 5,
      min: 0,
      step: 0.05,
    },
    minSize: 220,
    ...createRatingCell(mode, 'inst_feedback_mean_rating'),
  },
  {
    accessorKey: 'returns_mean_rating_bayesian_score',
    header: 'Returns Rating',
    filterVariant: 'range-slider',
    muiFilterSliderProps: {
      max: 5,
      min: 0,
      step: 0.05,
    },
    minSize: 220,
    ...createRatingCell(mode, 'returns_mean_rating'),
  },
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
