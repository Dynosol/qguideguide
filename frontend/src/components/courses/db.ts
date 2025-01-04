import Dexie, { Table } from 'dexie';

export interface Course {
  id: number;
  title: string;
  department: string;
  instructor: string;
  term: string;
  subject: string;
  blue_course_id: string;
  url: string;
  responses: number;
  invited_responses: number;
  response_ratio: number;
  course_mean_rating: number;
  materials_mean_rating: number;
  assignments_mean_rating: number;
  feedback_mean_rating: number;
  section_mean_rating: number;
  instructor_mean_rating: number;
  effective_mean_rating: number;
  accessible_mean_rating: number;
  enthusiasm_mean_rating: number;
  discussion_mean_rating: number;
  inst_feedback_mean_rating: number;
  returns_mean_rating: number;
  hours_mean_rating: number;
  recommend_mean_rating: number;
  number_comments: number;

  // **Additional Fields for Bayesian Ratings and Letter Grades**
  course_mean_rating_bayesian_score: number;
  course_mean_grade: string;
  materials_mean_rating_bayesian_score: number;
  materials_mean_grade: string;
  assignments_mean_rating_bayesian_score: number;
  assignments_mean_grade: string;
  feedback_mean_rating_bayesian_score: number;
  feedback_mean_grade: string;
  section_mean_rating_bayesian_score: number;
  section_mean_grade: string;
  instructor_mean_rating_bayesian_score: number;
  instructor_mean_grade: string;
  effective_mean_rating_bayesian_score: number;
  effective_mean_grade: string;
  accessible_mean_rating_bayesian_score: number;
  accessible_mean_grade: string;
  enthusiasm_mean_rating_bayesian_score: number;
  enthusiasm_mean_grade: string;
  discussion_mean_rating_bayesian_score: number;
  discussion_mean_grade: string;
  inst_feedback_mean_rating_bayesian_score: number;
  inst_feedback_mean_grade: string;
  returns_mean_rating_bayesian_score: number;
  returns_mean_grade: string;

  course_mean_rating_bayesian_score_department: number;
  course_mean_grade_department: string;
  materials_mean_rating_bayesian_score_department: number;
  materials_mean_grade_department: string;
  assignments_mean_rating_bayesian_score_department: number;
  assignments_mean_grade_department: string;
  feedback_mean_rating_bayesian_score_department: number;
  feedback_mean_grade_department: string;
  section_mean_rating_bayesian_score_department: number;
  section_mean_grade_department: string;
  instructor_mean_rating_bayesian_score_department: number;
  instructor_mean_grade_department: string;
  effective_mean_rating_bayesian_score_department: number;
  effective_mean_grade_department: string;
  accessible_mean_rating_bayesian_score_department: number;
  accessible_mean_grade_department: string;
  enthusiasm_mean_rating_bayesian_score_department: number;
  enthusiasm_mean_grade_department: string;
  discussion_mean_rating_bayesian_score_department: number;
  discussion_mean_grade_department: string;
  inst_feedback_mean_rating_bayesian_score_department: number;
  inst_feedback_mean_grade_department: string;
  returns_mean_rating_bayesian_score_department: number;
  returns_mean_grade_department: string;
}

/** Dexie database class */
class MyDatabase extends Dexie {
  /** Table for courses */
  courses!: Table<Course, number>;
  metadata!: Table<{ key: string; value: string }>;

  constructor() {
    super('MyCoursesDatabase');
    this.version(2).stores({
      // 'courses' is our table name, 'id' is the primary key.
      courses: 'id',
      metadata: 'key'
    });
    this.courses = this.table('courses');
  }
}

export const db = new MyDatabase();
