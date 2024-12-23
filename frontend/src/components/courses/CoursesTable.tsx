import React, { useEffect, useMemo, useState } from 'react';
import { MaterialReactTable, type MRT_ColumnDef } from 'material-react-table';
import axios from 'axios';

type Course = {
  id: number
  title: string
  department: string
  instructor: string
  term: string
  subject: string
  blue_course_id: string
  url: string
  responses: number
  invited_responses: number
  response_ratio: number
  course_mean_rating: number
  materials_mean_rating: number
  assignments_mean_rating: number
  feedback_mean_rating: number
  section_mean_rating: number
  instructor_mean_rating: number
  effective_mean_rating: number
  accessible_mean_rating: number
  enthusiasm_mean_rating: number
  discussion_mean_rating: number
  inst_feedback_mean_rating: number
  returns_mean_rating: number
  hours_mean_rating: number
  recommend_mean_rating: number
  number_comments: number
}

const CoursesTable: React.FC = () => {
  const [data, setData] = useState<Course[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/');
        setData(response.data.results);
      } catch (error) {
        console.error('Error fetching course data:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const columns = useMemo<MRT_ColumnDef<Course>[]>(
    () => [
      {
        accessorKey: 'title',
        header: 'Course Title',
      },
      {
        accessorKey: 'department',
        header: 'Department'
      },
      {
        accessorKey: 'instructor',
        header: 'Instructor'
      },
      {
        accessorKey: 'term',
        header: 'Term'
      },
      {
        accessorKey: 'blue_course_id',
        header: 'Blue Course ID',
      },
      {
        accessorKey: 'responses',
        header: 'Responses'
      },
      {
        accessorKey: 'invited_responses',
        header: 'Course Size'
      },
      {
        accessorKey: 'response_ratio',
        header: 'Response Rate',
        Cell: ({ cell }) => `${((cell.getValue() as number) * 100).toFixed(0)}%`
      },
      {
        accessorKey: 'course_mean_rating',
        header: 'Course Score'
      },
      {
        accessorKey: 'materials_mean_rating',
        header: 'Course Materials'
      },
      {
        accessorKey: 'assignments_mean_rating',
        header: 'Assignments Overall'
      },
      {
        accessorKey: 'feedback_mean_rating',
        header: 'Quality of Feedback'
      },
      {
        accessorKey: 'section_mean_rating',
        header: 'Section Rating'
      },
      {
        accessorKey: 'instructor_mean_rating',
        header: 'Instructor Overall'
      },
      {
        accessorKey: 'effective_mean_rating',
        header: 'Instructor Effectiveness'
      },
      {
        accessorKey: 'accessible_mean_rating',
        header: 'Instructor Accessibility'
      },
      {
        accessorKey: 'enthusiasm_mean_rating',
        header: 'Instructor Enthusiasm'
      },
      {
        accessorKey: 'discussion_mean_rating',
        header: 'Instructor Discussions'
      },
      {
        accessorKey: 'inst_feedback_mean_rating',
        header: 'Quality of Instructor Feedback'
      },
      {
        accessorKey: 'returns_mean_rating',
        header: 'Timely Assignment Returns'
      },
      {
        accessorKey: 'hours_mean_rating',
        header: 'Mean Hours'
      },
      {
        accessorKey: 'recommend_mean_rating',
        header: 'Mean Recommendation'
      },
      {
        accessorKey: 'number_comments',
        header: 'Number of Comments'
      },
      {
        accessorKey: 'url',
        header: 'QGuide Link',
        Cell: ({ cell }) => <a href={cell.getValue() as string}>QGuide Link</a>
      },
    ],
    []
  );

  return (
    <MaterialReactTable
      columns={columns}
      data={data}
      enableGlobalFilter
      enableSorting
      muiSearchTextFieldProps={{
        placeholder: 'Search...',
      }}
      muiPaginationProps={{
        rowsPerPageOptions: [10, 25, 50, 100, 250, 500, 1000, 5000, 10000, 50000],
        showFirstButton: false,
        showLastButton: false,
      }}
      initialState={{
        columnVisibility: {
          department: false,
          responses: false,
          response_ratio: false,
          blue_course_id: false,
          materials_mean_rating: false,
          assignments_mean_rating: false,
          feedback_mean_rating: false,
          section_mean_rating: false,
          effective_mean_rating: false,
          accessible_mean_rating: false,
          enthusiasm_mean_rating: false,
          discussion_mean_rating: false,
          inst_feedback_mean_rating: false,
          returns_mean_rating: false,
          hours_mean_rating: false,
          recommend_mean_rating: false,
          number_comments: false,
        },
        density: 'compact',
        showColumnFilters: true,
      }}
      state={{
        isLoading: loading, // Controls the loading state
        showLoadingOverlay: false, // Disables the loading overlay
      }}
      muiSkeletonProps={{
        animation: 'wave', // Optional: Customize skeleton animation
      }}
    />
  );
};

export default CoursesTable;
