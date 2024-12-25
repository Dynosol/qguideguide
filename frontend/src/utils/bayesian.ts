// bayesian.ts

import { db, Course } from '../components/courses/db';

/**
 * Define a union type for all aspects that require Bayesian calculations.
 */
type Aspect =
  | 'course_mean_rating'
  | 'materials_mean_rating'
  | 'assignments_mean_rating'
  | 'feedback_mean_rating'
  | 'section_mean_rating'
  | 'instructor_mean_rating'
  | 'effective_mean_rating'
  | 'accessible_mean_rating'
  | 'enthusiasm_mean_rating'
  | 'discussion_mean_rating'
  | 'inst_feedback_mean_rating'
  | 'returns_mean_rating'
  | 'hours_mean_rating'
  | 'recommend_mean_rating';

/**
 * Interface to hold global statistics for each aspect.
 */
interface AspectStats {
  m: number; // Global mean rating
  C: number; // Average number of responses
}

/**
 * Define grade boundaries for letter grades based on percentile ranks.
 */
const grade_boundaries: Array<{ lower: number; upper: number; grade: string }> = [
  { lower: 99.99, upper: 100, grade: 'S+' },
  { lower: 99.5, upper: 99.9, grade: 'S' },
  { lower: 99, upper: 99.5, grade: 'S-' },
  { lower: 98, upper: 99, grade: 'A+' },
  { lower: 95, upper: 98, grade: 'A' },
  { lower: 90, upper: 95, grade: 'A-' },
  { lower: 80, upper: 90, grade: 'B+' },
  { lower: 60, upper: 80, grade: 'B' },
  { lower: 50, upper: 60, grade: 'B-' },
  { lower: 40, upper: 50, grade: 'C+' },
  { lower: 30, upper: 40, grade: 'C' },
  { lower: 20, upper: 30, grade: 'C-' },
  { lower: 10, upper: 20, grade: 'D' },
  { lower: 0, upper: 10, grade: 'F' },
];

/**
 * Assign a letter grade based on the percentile rank.
 * @param percentile - The percentile rank (0 to 100).
 * @returns The corresponding letter grade.
 */
const assignLetterGrade = (percentile: number): string => {
  for (const boundary of grade_boundaries) {
    if (boundary.lower <= percentile && percentile < boundary.upper) {
      return boundary.grade;
    }
  }
  return 'F'; // Default grade
};

/**
 * Compute the percentile rank of a value within a sorted array.
 * @param value - The value to find the percentile for.
 * @param sortedValues - The sorted array of values.
 * @returns The percentile rank (0 to 100).
 */
const getPercentile = (value: number, sortedValues: number[]): number => {
  if (sortedValues.length === 0) return 0;
  let count = 0;
  for (const sortedValue of sortedValues) {
    if (sortedValue < value) {
      count++;
    }
  }
  return (count / sortedValues.length) * 100;
};

/**
 * Helper function to compute Bayesian ratings and assign letter grades.
 */
export const computeAndStoreBayesianRatings = async (): Promise<void> => {
  // Fetch all courses from Dexie
  const courses: Course[] = await db.courses.toArray();
  if (courses.length === 0) return;

  // Define the aspects to compute Bayesian ratings for
  const aspects: Aspect[] = [
    'course_mean_rating',
    'materials_mean_rating',
    'assignments_mean_rating',
    'feedback_mean_rating',
    'section_mean_rating',
    'instructor_mean_rating',
    'effective_mean_rating',
    'accessible_mean_rating',
    'enthusiasm_mean_rating',
    'discussion_mean_rating',
    'inst_feedback_mean_rating',
    'returns_mean_rating',
    'hours_mean_rating',
    'recommend_mean_rating',
  ];

  // Calculate global mean (m) and average responses (C) for each aspect
  const aspectStats: Record<Aspect, AspectStats> = {} as Record<Aspect, AspectStats>;

  aspects.forEach((aspect) => {
    let sumRatings = 0;
    let countRatings = 0;
    let sumResponses = 0;

    courses.forEach((course) => {
      const rating = course[aspect];
      if (typeof rating === 'number' && !isNaN(rating)) {
        sumRatings += rating;
        countRatings += 1;
      }
      sumResponses += course.responses || 0;
    });

    const m = countRatings > 0 ? sumRatings / countRatings : 0;
    const C = courses.length > 0 ? sumResponses / courses.length : 0;

    aspectStats[aspect] = { m, C };
  });

  // Compute Bayesian scores for each course and aspect
  const updatedCourses: Course[] = courses.map((course) => {
    const updatedCourse: Course = { ...course };
    aspects.forEach((aspect) => {
      const mean = course[aspect];
      const N = course.responses || 0;
      const { m, C } = aspectStats[aspect];
      const bayesian = (C * m + mean * N) / (C + N);
      updatedCourse[`${aspect}_bayesian`] = isNaN(bayesian) ? 'No Data' : bayesian.toFixed(2);
    });
    return updatedCourse;
  });

  // For each aspect, compute percentile ranks and assign letter grades
  aspects.forEach((aspect) => {
    // Extract all valid Bayesian ratings for this aspect
    const bayesianValues: number[] = updatedCourses
      .map((course) => parseFloat(course[`${aspect}_bayesian`] || '0'))
      .filter((value) => !isNaN(value));

    // Sort the Bayesian ratings in ascending order
    const sortedBayesian = [...bayesianValues].sort((a, b) => a - b);

    // Assign letter grades based on percentile rank
    updatedCourses.forEach((course) => {
      const bayesianStr = course[`${aspect}_bayesian`];
      if (bayesianStr && bayesianStr !== 'No Data') {
        const bayesian = parseFloat(bayesianStr);
        const percentile = getPercentile(bayesian, sortedBayesian);
        const letterGrade = assignLetterGrade(percentile);
        course[`${aspect}_letter_grade`] = letterGrade;
      } else {
        course[`${aspect}_letter_grade`] = 'No Data';
      }
    });
  });

  // Bulk update the courses in Dexie with Bayesian ratings and letter grades
  await db.courses.bulkPut(updatedCourses);
};
