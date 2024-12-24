import React, { useEffect, useMemo, useState } from 'react';
import {
  MaterialReactTable,
  useMaterialReactTable,
  type MRT_ColumnDef,
  MRT_FilterRangeSlider,
} from 'material-react-table';
import axios from 'axios';
import { db, Course } from './db';
import { googleSearchFilter } from '../../utils/searchHelper';

const USER_KEYPRESS_SEARCHDELAY = 100 // in milliseconds

const CoursesTable: React.FC = () => {
  // Things that change
  const [data, setData] = useState<Course[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchValue, setSearchValue] = useState(''); // this one changes every keystroke, but doesn't update after each to lag everything
  const [globalFilter, setGlobalFilter] = useState('');

  /**
   * Attempt to load any existing data from Dexie. If none found, fetch from server.
   */
  useEffect(() => {
    (async () => {
      try {
        // 1. Check how many courses are stored in Dexie
        const count = await db.courses.count();
        if (count === 0) {
          // 2. Nothing in Dexie => fetch from the server
          await fetchAndStoreCourses();
        } else {
          // 3. We have data => load from Dexie
          const storedCourses = await db.courses.toArray();
          console.log('Courses loaded from IndexedDB:', storedCourses); // so we know it worked
          setData(storedCourses);
          setIsLoading(false);
        }
      } catch (error) {
        console.error('Error loading from Dexie', error);
        setIsLoading(false);
      }
    })();
  }, []);

  // wait one second after the user's last keypress
  useEffect(() => {
    const timer = setTimeout(() => {
      setGlobalFilter(searchValue);
    }, USER_KEYPRESS_SEARCHDELAY);
    return () => clearTimeout(timer);
  }, [searchValue, globalFilter]);

  /**
   * Fetch from server, then store in Dexie
   */
  const fetchAndStoreCourses = async () => {
    setIsLoading(true);
    try {
      const response = await axios.get<Course[]>('http://localhost:8000/api/');
      const courses: Course[] = response.data;

      // put in React state
      setData(courses);

      // store in Dexie
      // first clear existing data (if any)
      await db.courses.clear();
      // then bulkAdd
      await db.courses.bulkAdd(courses);
      console.log('Courses successfully stored in IndexedDB'); // so we know it worked
    } catch (error) {
      console.error('Error fetching or storing courses:', error);
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * OPTIONAL REFRESH CLEARING??
   */
  // const handleRefresh = async () => {
  //   await db.courses.clear();
  //   await fetchAndStoreCourses();
  // };

  const columns = useMemo<MRT_ColumnDef<Course>[]>(
    () => [
      {
        accessorKey: 'title',
        header: 'Course Title',
        filterFn: googleSearchFilter,
        minSize: 400,
      },
      {
        accessorKey: 'department',
        header: 'Department',
        filterFn: googleSearchFilter,
        filterVariant: 'multi-select',
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
        Cell: ({ cell }) =>
          `${((cell.getValue() as number) * 100).toFixed(0)}%`,
        minSize: 250,
        filterVariant: 'range-slider',
        muiFilterSliderProps: {
          max: 1, // Maximum percentage
          min: 0,   // Minimum percentage
          step: 0.01,  // Step in whole percentages
          valueLabelFormat: (value) => `${(value * 100).toFixed(0)}%`, // Format value as percentage
        },
      },
      {
        accessorKey: 'course_mean_rating',
        header: 'Course Score',
        filterVariant: 'range-slider',
        muiFilterSliderProps: {
          max: 5, //custom max (as opposed to faceted max)
          min: 0, //custom min (as opposed to faceted min)
          step: 0.1,
        },
        minSize: 200,
      },
      {
        accessorKey: 'materials_mean_rating',
        header: 'Course Materials',
        minSize: 250,
        filterVariant: 'range-slider',
        muiFilterSliderProps: {
          max: 5, //custom max (as opposed to faceted max)
          min: 0, //custom min (as opposed to faceted min)
          step: 0.1,
        },
      },
      {
        accessorKey: 'assignments_mean_rating',
        header: 'Assignments Quality',
        minSize: 250,
        filterVariant: 'range-slider',
        muiFilterSliderProps: {
          max: 5, //custom max (as opposed to faceted max)
          min: 0, //custom min (as opposed to faceted min)
          step: 0.1,
        },
      },
      {
        accessorKey: 'feedback_mean_rating',
        header: 'Quality of Feedback',
        minSize: 250,
        filterVariant: 'range-slider',
        muiFilterSliderProps: {
          max: 5, //custom max (as opposed to faceted max)
          min: 0, //custom min (as opposed to faceted min)
          step: 0.1,
        },
      },
      {
        accessorKey: 'section_mean_rating',
        header: 'Section Rating',
        minSize: 200,
        filterVariant: 'range-slider',
        muiFilterSliderProps: {
          max: 5, //custom max (as opposed to faceted max)
          min: 0, //custom min (as opposed to faceted min)
          step: 0.1,
        },
      },
      {
        accessorKey: 'instructor_mean_rating',
        header: 'Instructor Score',
        minSize: 230,
        filterVariant: 'range-slider',
        muiFilterSliderProps: {
          max: 5, //custom max (as opposed to faceted max)
          min: 0, //custom min (as opposed to faceted min)
          step: 0.1,
        },
      },
      {
        accessorKey: 'effective_mean_rating',
        header: 'Instructor Effectiveness',
        minSize: 250,
        filterVariant: 'range-slider',
        muiFilterSliderProps: {
          max: 5, //custom max (as opposed to faceted max)
          min: 0, //custom min (as opposed to faceted min)
          step: 0.1,
        },
      },
      {
        accessorKey: 'accessible_mean_rating',
        header: 'Instructor Accessibility',
        minSize: 250,
        filterVariant: 'range-slider',
        muiFilterSliderProps: {
          max: 5, //custom max (as opposed to faceted max)
          min: 0, //custom min (as opposed to faceted min)
          step: 0.1,
        },
      },
      {
        accessorKey: 'enthusiasm_mean_rating',
        header: 'Instructor Enthusiasm',
        minSize: 250,
        filterVariant: 'range-slider',
        muiFilterSliderProps: {
          max: 5, //custom max (as opposed to faceted max)
          min: 0, //custom min (as opposed to faceted min)
          step: 0.1,
        },
      },
      {
        accessorKey: 'discussion_mean_rating',
        header: 'Instructor Discussions',
        minSize: 250,
        filterVariant: 'range-slider',
        muiFilterSliderProps: {
          max: 5, //custom max (as opposed to faceted max)
          min: 0, //custom min (as opposed to faceted min)
          step: 0.1,
        },
      },
      {
        accessorKey: 'inst_feedback_mean_rating',
        header: 'Quality of Instructor Feedback',
        minSize: 300,
        filterVariant: 'range-slider',
        muiFilterSliderProps: {
          max: 5, //custom max (as opposed to faceted max)
          min: 0, //custom min (as opposed to faceted min)
          step: 0.1,
        },
      },
      {
        accessorKey: 'returns_mean_rating',
        header: 'Timely Assignment Returns',
        minSize: 270,
        filterVariant: 'range-slider',
        muiFilterSliderProps: {
          max: 5, //custom max (as opposed to faceted max)
          min: 0, //custom min (as opposed to faceted min)
          step: 0.1,
        },
      },
      {
        accessorKey: 'hours_mean_rating',
        header: 'Mean Hours',
        filterVariant: 'range-slider',
        muiFilterSliderProps: {
          step: 0.1,
        },
      },
      {
        accessorKey: 'recommend_mean_rating',
        header: 'Mean Recommendation',
        minSize: 250,
        filterVariant: 'range-slider',
        muiFilterSliderProps: {
          max: 5, //custom max (as opposed to faceted max)
          min: 0, //custom min (as opposed to faceted min)
          step: 0.1,
        },
      },
      {
        accessorKey: 'number_comments',
        header: 'Number of Comments',
        minSize: 250,
        filterVariant: 'range',
      },
      {
        accessorKey: 'url',
        header: 'QGuide Link',
        minSize: 200,
        Cell: ({ cell }) => {
          const url = cell.getValue() as string;
          return (
              <a href={url} target="_blank" rel="noreferrer">
                QGuide Link
              </a>
          );
        },
      }
    ],
    []
  );

  const table = useMaterialReactTable({
    columns,
    data,
    state: {
      isLoading,
      globalFilter,
    },
    enableGlobalFilter: true, // big search box at the top
    enableSorting: true,
    positionGlobalFilter: 'left',
    muiSearchTextFieldProps: {
      placeholder: 'Search all fields...',
      variant: 'outlined',
      value: searchValue ?? '',
      onChange: (event) => {
        setSearchValue(event.target.value);
        console.info('Global search text:', event.target.value);
      },
    },
    onGlobalFilterChange: (newValue) => { // forcing syncing, so the "clear search" button works
      console.log("onGlobalFilterChange", newValue);
      setGlobalFilter(newValue);
      setSearchValue(newValue);
    },
    muiPaginationProps: {
      rowsPerPageOptions: [
        10, 25, 50, 100, 250, 500, 1000, 5000, 11961,
      ],
      showFirstButton: true,
      showLastButton: true,
    },
    enableColumnPinning: true,
    enableFacetedValues: true,
    initialState: {
      columnPinning: {
        left: ['title'],
      },
      columnVisibility: {
        // url: false,
        // // department: false,
        // responses: false,
        // response_ratio: false,
        // blue_course_id: false,
        // materials_mean_rating: false,
        // assignments_mean_rating: false,
        // feedback_mean_rating: false,
        // section_mean_rating: false,
        // effective_mean_rating: false,
        // accessible_mean_rating: false,
        // enthusiasm_mean_rating: false,
        // discussion_mean_rating: false,
        // inst_feedback_mean_rating: false,
        // returns_mean_rating: false,
        // hours_mean_rating: false,
        // recommend_mean_rating: false,
        // number_comments: false,
      },
      density: 'comfortable',
      showColumnFilters: true,
      showGlobalFilter: true,
    },
    muiSkeletonProps: {
      animation: 'wave',
    },
    enableRowVirtualization: true,
    enablePagination: true,
    muiTableBodyRowProps: ({ row }) => ({
      onClick: () => {
        const { url } = row.original;
        if (url) {
          window.open(url, '_blank'); // Opens the qguide page in a new tab
        } else {
          console.warn('No URL found for the selected row');
        }
      },
      sx: { cursor: 'pointer' }, // Change the cursor to indicate clickability
    }),
  });

  return <MaterialReactTable table={table} />;
};

export default CoursesTable;
