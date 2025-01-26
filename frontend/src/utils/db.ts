import Dexie, { Table } from 'dexie';

export interface Course {
  // ...your course interface
}

export class QGuideGuideDB extends Dexie {
  courses!: Table<Course>;

  constructor() {
    super('QGuideGuideDB');
    this.version(1).stores({
      courses: '++id, title, department, instructor', // Add appropriate indexes
    });
  }
}

export const db = new QGuideGuideDB();
