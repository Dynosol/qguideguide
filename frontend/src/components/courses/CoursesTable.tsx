// src/components/CoursesTable/CoursesTable.tsx

import React, { useEffect, useMemo, useState } from 'react';
import {
  MaterialReactTable,
  useMaterialReactTable,
  type MRT_ColumnDef,
} from 'material-react-table';
import axios from 'axios';
import { db, Course } from './db';
import { useThemeContext } from '../../utils/themeHelper';
import { createTheme, ThemeProvider as MuiThemeProvider } from '@mui/material/styles';
import { colorPalettes } from '../../utils/colors';
import { getCoursesColumns } from './columns'; // Import the columns

const USER_KEYPRESS_SEARCHDELAY = 100; // in milliseconds
interface CoursesTableProps {
  position: string; // Add position prop
}

const CoursesTable: React.FC<CoursesTableProps> = ({ position }) => {
  const { mode } = useThemeContext();
  const [data, setData] = useState<Course[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchValue, setSearchValue] = useState('');
  const [globalFilter, setGlobalFilter] = useState('');
  const [columnPinning, setColumnPinning] = useState<{ left?: string[] }>({ left: ['title'] });

  const tableTheme = useMemo(
    () =>
      createTheme({
        palette: {
          mode: mode,
          primary: {
            main: colorPalettes[mode].harvard,
          },
          ...(mode === 'dark'
            ? {
                text: {
                  primary: colorPalettes[mode].textColorDark,
                },
              }
            : {
                text: {
                  primary: '#000000',
                },
              }),
        },
      }),
    [mode]
  );

  // Load data from IndexedDB or fetch from server
  useEffect(() => {
    (async () => {
      try {
        const count = await db.courses.count();
        if (count === 0) {
          await fetchAndStoreCourses();
        } else {
          const storedCourses = await db.courses.toArray();
          setData(storedCourses);
          setIsLoading(false);
        }
      } catch (error) {
        console.error('Error loading from Dexie', error);
        setIsLoading(false);
      }
    })();
  }, []);

  // Debounce search input
  useEffect(() => {
    const timer = setTimeout(() => {
      setGlobalFilter(searchValue);
    }, USER_KEYPRESS_SEARCHDELAY);
    return () => clearTimeout(timer);
  }, [searchValue]);

  // Adjust columnPinning based on window size
  useEffect(() => {
    const updateColumnPinning = () => {
      if (window.innerWidth <= 850) {
        setColumnPinning({});
      } else {
        setColumnPinning({ left: ['title'] });
      }
    };

    updateColumnPinning();
    window.addEventListener('resize', updateColumnPinning);
    return () => window.removeEventListener('resize', updateColumnPinning);
  }, []);

  // Fetch and store courses
  const fetchAndStoreCourses = async () => {
    setIsLoading(true);
    try {
      const response = await axios.get<Course[]>('http://localhost:8000/api/courses/');
      const courses: Course[] = response.data;

      await db.courses.clear();
      await db.courses.bulkAdd(courses);
      // console.log('Courses successfully stored in IndexedDB');

      setData(courses);
    } catch (error) {
      console.error('Error fetching or storing courses:', error);
    } finally {
      setIsLoading(false);
    }
  };

  // Import columns using the helper function
  const columns = useMemo<MRT_ColumnDef<Course>[]>(
    () => getCoursesColumns(mode, position),
    [mode, position]
  );

  const table = useMaterialReactTable({
    columns,
    data,
    state: {
      isLoading,
      globalFilter,
      columnPinning,
    },
    enableGlobalFilter: true,
    enableSorting: true,
    positionGlobalFilter: 'left',
    muiSearchTextFieldProps: {
      placeholder: 'Search all fields...',
      variant: 'outlined',
      value: searchValue ?? '',
      onChange: (event) => {
        setSearchValue(event.target.value);
      },
    },
    onGlobalFilterChange: (newValue) => {
      setGlobalFilter(newValue);
      setSearchValue(newValue);
    },
    muiPaginationProps: {
      rowsPerPageOptions: [10, 25, 50, 100, 250, 500, 1000, 5000, 11608],
      showFirstButton: true,
      showLastButton: true,
    },
    enableColumnPinning: true,
    enableFacetedValues: true,
    initialState: {
      columnVisibility: {
        responses: false,
        response_ratio: false,
        blue_course_id: false,

        materials_mean_rating: false,
        materials_mean_rating_bayesian_score: false,
        materials_mean_rating_bayesian_score_department: false,

        feedback_mean_rating: false,
        feedback_mean_rating_bayesian_score: false,
        feedback_mean_rating_bayesian_score_department: false,

        effective_mean_rating: false,
        effective_mean_rating_bayesian_score: false,
        effective_mean_rating_bayesian_score_department: false,

        accessible_mean_rating: false,
        accessible_mean_rating_bayesian_score: false,
        accessible_mean_rating_bayesian_score_department: false,

        enthusiasm_mean_rating: false,
        enthusiasm_mean_rating_bayesian_score: false,
        enthusiasm_mean_rating_bayesian_score_department: false,

        discussion_mean_rating: false,
        discussion_mean_rating_bayesian_score: false,
        discussion_mean_rating_bayesian_score_department: false,

        inst_feedback_mean_rating: false,
        inst_feedback_mean_rating_bayesian_score: false,
        inst_feedback_mean_rating_bayesian_score_department: false,

        returns_mean_rating: false,
        returns_mean_rating_bayesian_score: false,
        returns_mean_rating_bayesian_score_department: false,

        
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
          window.open(url, '_blank');
        } else {
          console.warn('No URL found for the selected row');
        }
      },
      sx: {
        cursor: 'pointer',
      },
    }),
    muiTableContainerProps: { sx: { maxHeight: '79vh' } },
    // muiTableBodyProps: {
    //   sx: {
    //     '& tr:nth-of-type(odd) > td': {
    //       backgroundColor: colorPalettes[mode].stripes,
    //     },
    //   },
    // },
  });

  return (
    <MuiThemeProvider theme={tableTheme}>
      <MaterialReactTable table={table} />
    </MuiThemeProvider>
  );
};

export default CoursesTable;
