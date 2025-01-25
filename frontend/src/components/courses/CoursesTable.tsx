// src/components/CoursesTable/CoursesTable.tsx

import React, { useEffect, useMemo, useState } from 'react';
import {
  MaterialReactTable,
  useMaterialReactTable,
  type MRT_ColumnDef,
} from 'material-react-table';
import { db, Course } from './db';
import { useThemeContext } from '../../utils/themeHelper';
import { createTheme, ThemeProvider as MuiThemeProvider } from '@mui/material/styles';
import { colorPalettes } from '../../utils/colors';
import { getCoursesColumns } from './Columns'; // Import the columns
import { fetchCourses } from '../../utils/api';
import axios from 'axios'; // Import axios
import config from '../../config';
import AuthService from '../../utils/auth'; // Import AuthService

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

  // Load data with stale-while-revalidate pattern
  useEffect(() => {
    const initializeAndFetchData = async () => {
      try {
        setIsLoading(true);
        // Initialize auth before making API calls
        await AuthService.getInstance().initialize();
        const cachedCourses = await db.courses.toArray();
        const metadata = await db.metadata.get('etags');
        
        // If we have cached data, show it immediately
        if (cachedCourses.length > 0) {
          setData(cachedCourses);
          setIsLoading(false);
        }

        // Prepare headers for conditional request
        const headers: Record<string, string> = {};
        if (metadata?.coursesEtag) {
          headers['If-None-Match'] = metadata.coursesEtag;
        }

        // Fetch fresh data in the background
        const response = await fetchCourses(headers);
        
        // Only update if we got new data (not 304)
        if (response.status !== 304) {
          const courses = Array.isArray(response.data) ? response.data :
                       (response.data.results ? response.data.results : []);

          if (courses.length > 0) {
            setData(courses);
            
            // Update IndexedDB
            await db.transaction('rw', db.courses, async () => {
              await db.courses.clear();
              await db.courses.bulkAdd(courses);
            });

            // Store new ETag
            await db.metadata.put({
              key: 'etags',
              value: {
                ...metadata?.value,
                coursesEtag: response.headers.etag,
                lastUpdate: new Date().toISOString()
              }
            });
          }
        }
      } catch (error) {
        console.error('Error fetching or storing courses:', error);
        if (axios.isAxiosError(error)) {
          console.error('Axios error details:', {
            response: error.response?.data,
            status: error.response?.status,
            headers: error.response?.headers,
            config: error.config
          });
        }
      } finally {
        setIsLoading(false);
      }
    };

    initializeAndFetchData();
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
