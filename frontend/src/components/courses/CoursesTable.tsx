import React, { useEffect, useMemo, useState } from 'react';
import { MaterialReactTable, type MRT_ColumnDef } from 'material-react-table';
import axios from 'axios';

// Define the type for your course data
type Course = {
  id: number;
  title: string;
  department: string;
  instructor: string;
  term: string;
  class_size: number;
  rating: number;
  hours: number;
  instructor_rating: number;
  instructor_dept_rating: number;
  qguide_link: string;
};

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
        header: 'Title',
        size: 200,
      },
      {
        accessorKey: 'department',
        header: 'Department',
        size: 150,
      },
      {
        accessorKey: 'instructor',
        header: 'Instructor',
        size: 150,
      },
      {
        accessorKey: 'term',
        header: 'Term',
        size: 100,
      },
      {
        accessorKey: 'class_size',
        header: 'Class Size',
        size: 100,
      },
      {
        accessorKey: 'rating',
        header: 'Rating',
        size: 100,
      },
      {
        accessorKey: 'hours',
        header: 'Hours',
        size: 100,
      },
      {
        accessorKey: 'instructor_rating',
        header: 'Instructor Rating',
        size: 150,
      },
      {
        accessorKey: 'instructor_dept_rating',
        header: 'Instructor Dept. Rating',
        size: 150,
      },
      {
        accessorKey: 'qguide_link',
        header: 'QGuide Link',
        Cell: ({ cell }) => (
          <a
            href={cell.getValue<string>()}
            target="_blank"
            rel="noopener noreferrer"
          >
            Link
          </a>
        ),
        size: 200,
      },
    ],
    []
  );

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="p-4">
      <MaterialReactTable
        columns={columns}
        data={data}
        enableGlobalFilter
        enableSorting
        muiSearchTextFieldProps={{
          placeholder: 'Search...',
        }}
      />
    </div>
  );
};

export default CoursesTable;
