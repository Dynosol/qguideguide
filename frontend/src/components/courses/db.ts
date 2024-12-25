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
    course_mean_rating_bayesian?: string;
    course_mean_rating_letter_grade?: string;
    materials_mean_rating_bayesian?: string;
    materials_mean_rating_letter_grade?: string;
    assignments_mean_rating_bayesian?: string;
    assignments_mean_rating_letter_grade?: string;
    feedback_mean_rating_bayesian?: string;
    feedback_mean_rating_letter_grade?: string;
    section_mean_rating_bayesian?: string;
    section_mean_rating_letter_grade?: string;
    instructor_mean_rating_bayesian?: string;
    instructor_mean_rating_letter_grade?: string;
    effective_mean_rating_bayesian?: string;
    effective_mean_rating_letter_grade?: string;
    accessible_mean_rating_bayesian?: string;
    accessible_mean_rating_letter_grade?: string;
    enthusiasm_mean_rating_bayesian?: string;
    enthusiasm_mean_rating_letter_grade?: string;
    discussion_mean_rating_bayesian?: string;
    discussion_mean_rating_letter_grade?: string;
    inst_feedback_mean_rating_bayesian?: string;
    inst_feedback_mean_rating_letter_grade?: string;
    returns_mean_rating_bayesian?: string;
    returns_mean_rating_letter_grade?: string;
    hours_mean_rating_bayesian?: string;
    hours_mean_rating_letter_grade?: string;
    recommend_mean_rating_bayesian?: string;
    recommend_mean_rating_letter_grade?: string;
  }

  /** Dexie database class */
  class MyDatabase extends Dexie {
    /** Table for courses */
    courses!: Table<Course, number>;

    constructor() {
      super('MyCoursesDatabase');
      this.version(1).stores({
        // 'courses' is our table name, 'id' is the primary key.
        courses: 'id',
      });
      this.courses = this.table('courses');
    }
  }

  export const db = new MyDatabase();
