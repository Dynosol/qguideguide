import Dexie, { Table } from 'dexie';

export interface Professor {
  id: number;
  name: string;
  departments: string;
  total_ratings: number;
  empirical_bayes_average: number;
  empirical_bayes_rank: number;
  overall_letter_grade: string;
  intra_department_eb_average: number;
  intra_department_letter_grade: string;
  intra_department_ranks: string;
  lastUpdated?: string;
}

export interface Department {
  id: number;
  name: string;
  mean_empirical_bayes_average: number;
  mean_empirical_bayes_rank: number;
}

export class ProfessorDatabase extends Dexie {
  professors!: Table<Professor>;
  departments!: Table<Department>;
  metadata!: Table<{ key: string; value: any }>;

  constructor() {
    super('professorsDatabase');
    this.version(2).stores({
      professors: '++id, name, departments, empirical_bayes_rank',
      departments: '++id, name, mean_empirical_bayes_average, mean_empirical_bayes_rank',
      metadata: 'key'
    });
  }
}

export const db = new ProfessorDatabase();
