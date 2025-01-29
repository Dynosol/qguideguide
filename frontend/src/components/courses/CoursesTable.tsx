// src/components/CoursesTable/CoursesTable.tsx

import React, { useEffect, useMemo, useState, useCallback, useRef } from 'react';
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
// import axios from 'axios'; // Import axios
// import config from '../../config';

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
  const [departments, setDepartments] = useState<string[]>([]);
  const [terms, setTerms] = useState<string[]>([]);

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

  // Load all data at once
  useEffect(() => {
    const loadData = async () => {
      setIsLoading(true);
      try {
        // Try to get data from IndexedDB first
        const cachedData = await db.courses.toArray();
        
        if (cachedData && cachedData.length > 0) {
          console.log('Loading data from cache...');
          setData(cachedData);
          setIsLoading(false);
        }

        // Always fetch fresh data from API
        console.log('Fetching fresh data...');
        const response = await fetchCourses();
        const freshData = response.data;

        // Update state with fresh data
        setData(freshData);
        
        // Update cache with fresh data
        await db.transaction('rw', db.courses, async () => {
          await db.courses.clear(); // Clear old cache
          await db.courses.bulkAdd(freshData);
        });
        
      } catch (error) {
        console.error('Error loading courses:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadData();
  }, [position]); // Reload when position changes

  // Extract unique departments from data
  useEffect(() => {
    const uniqueDepartments = data.map(course => course.department);
    const uniqueDeptSet = new Set(uniqueDepartments);
    setDepartments(Array.from(uniqueDeptSet));
  }, [data]);

  useEffect(() => {
    const uniqueTerms = data.map(course => course.term);
    const uniqueTermSet = new Set(uniqueTerms);
    setTerms(Array.from(uniqueTermSet));
  }, [data]);


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
    () => getCoursesColumns(mode, position, departments, terms),
    [mode, position, departments, terms]
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
    enablePagination: false,
    enableRowVirtualization: true,
    virtualizationOptions: {
      overscan: 25,
    },
    enableToolbarBottom: true,
    enableToolbarTop: true,
    enableColumnFilters: true,
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
    muiTableContainerProps: {
      sx: { 
        maxHeight: '79vh',
        overflowY: 'auto',
      },
    },
    renderBottomToolbarCustomActions: () => (
      <div style={{ padding: '8px', display: 'flex', justifyContent: 'space-between', width: '100%' }}>
        <div>
          {isLoading ? 'Loading courses...' : "Courses loaded from Fall '19 - Spring '23"}
        </div>
        <div>
          {isLoading ? '' : `Loaded ${data.length} historical courses`}
        </div>
      </div>
    ),
  });

  return (
    <MuiThemeProvider theme={tableTheme}>
      <MaterialReactTable table={table} />
    </MuiThemeProvider>
  );
};

export default CoursesTable;