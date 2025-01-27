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
import axios from 'axios'; // Import axios
import config from '../../config';

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
  const [pagination, setPagination] = useState({
    pageIndex: 0,
    pageSize: 100,
  });
  const [rowCount, setRowCount] = useState(0);

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

  // Load data with pagination
  useEffect(() => {
    const loadData = async () => {
      setIsLoading(true);
      try {
        // Calculate page number (1-based for backend)
        const page = pagination.pageIndex + 1;
        const pageSize = pagination.pageSize;

        const response = await fetchCourses(page, pageSize);
        const { results, count } = response.data;
        
        setData(results);
        setRowCount(count);
      } catch (error) {
        console.error('Error loading courses:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadData();
  }, [pagination.pageIndex, pagination.pageSize, position]);

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
      pagination,
    },
    enableGlobalFilter: true,
    enableSorting: true,
    manualPagination: true,
    rowCount,
    onPaginationChange: setPagination,
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
    enablePagination: true,
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
      <div style={{ padding: '8px' }}>
        {isLoading ? 'Loading courses... this might take a while...' : `Showing ${pagination.pageIndex * pagination.pageSize + 1} - ${Math.min((pagination.pageIndex + 1) * pagination.pageSize, rowCount)} of ${rowCount} courses`}
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
