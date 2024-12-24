import { Row, FilterFn } from '@tanstack/react-table';

/**
 * A tokenized representation of the search query.
 */
export interface SearchToken {
  value: string; // The raw text or value of the token
  type:
    | 'PHRASE'
    | 'WORD'
    | 'EXCLUDE'
    | 'REQUIRED'
    | 'BOOLEAN_AND'
    | 'BOOLEAN_OR'
    | 'BOOLEAN_NOT'
    | 'REGEX'
    | 'WILDCARD'
    | 'NUMERIC_RANGE'
    | 'DATE_RANGE'
    | 'PROXIMITY'
    | 'GROUP_START'
    | 'GROUP_END';
  range?: { lower: string; upper: string }; // Numeric or date range bounds
  proximityDistance?: number; // Distance for proximity search
}

/**
 * Parses the search query into tokens (quoted phrases, wildcards, etc.).
 */
export function parseSearchQuery(query: string): SearchToken[] {
  const tokens: SearchToken[] = [];
  const regex =
    /\(|\)|"[^"]+"~\d+|"[^"]+"|(?:(?:^|\s)(AND|OR|NOT)(?=\s|$))|[-+][^\s]+|([a-zA-Z0-9_]+):(\d{4}-\d{2}-\d{2}\.\.\d{4}-\d{2}-\d{2}|\d+\.\.\d+|("[^"]+"|\S+))|regex:\/([^/]+)\/|[\w*?]+|\S+/gi;

  let match;
  while ((match = regex.exec(query)) !== null) {
    const [fullMatch] = match;

    // Parentheses
    if (fullMatch === '(') {
      tokens.push({ value: '(', type: 'GROUP_START' });
      continue;
    }
    if (fullMatch === ')') {
      tokens.push({ value: ')', type: 'GROUP_END' });
      continue;
    }

    // Proximity
    const proximityMatch = fullMatch.match(/^"([^"]+)"~(\d+)$/);
    if (proximityMatch) {
      tokens.push({
        value: proximityMatch[1],
        type: 'PROXIMITY',
        proximityDistance: parseInt(proximityMatch[2], 10),
      });
      continue;
    }

    // Quoted phrase
    const phraseMatch = fullMatch.match(/^"([^"]+)"$/);
    if (phraseMatch) {
      tokens.push({ value: phraseMatch[1], type: 'PHRASE' });
      continue;
    }

    // Boolean operators
    const booleanOp = fullMatch.toUpperCase();
    if (['AND', 'OR', 'NOT'].includes(booleanOp)) {
      tokens.push({ value: booleanOp, type: `BOOLEAN_${booleanOp}` as any });
      continue;
    }

    // Minus or plus prefix
    if (/^-[^\s]+/.test(fullMatch)) {
      tokens.push({ value: fullMatch.slice(1), type: 'EXCLUDE' });
      continue;
    }
    if (/^\+[^\s]+/.test(fullMatch)) {
      tokens.push({ value: fullMatch.slice(1), type: 'REQUIRED' });
      continue;
    }

    // Regex
    const regexMatch = fullMatch.match(/^regex:\/([^/]+)\/$/);
    if (regexMatch) {
      tokens.push({ value: regexMatch[1], type: 'REGEX' });
      continue;
    }

    // Wildcards
    if (fullMatch.includes('*') || fullMatch.includes('?')) {
      tokens.push({ value: fullMatch, type: 'WILDCARD' });
      continue;
    }

    // Default: Treat as a word
    tokens.push({ value: fullMatch, type: 'WORD' });
  }

  return tokens;
}

/**
 * Evaluates tokens against the value of a single cell.
 */
function evaluateTokens(tokens: SearchToken[], cellValue: string): boolean {
  const lowerValue = cellValue.toLowerCase();

  for (const token of tokens) {
    switch (token.type) {
      case 'PHRASE':
        if (!lowerValue.includes(token.value.toLowerCase())) return false;
        break;
      case 'WORD':
        if (!lowerValue.includes(token.value.toLowerCase())) return false;
        break;
      case 'EXCLUDE':
        if (lowerValue.includes(token.value.toLowerCase())) return false;
        break;
      case 'REQUIRED':
        if (!lowerValue.includes(token.value.toLowerCase())) return false;
        break;
      case 'REGEX': {
        const regex = new RegExp(token.value, 'i');
        if (!regex.test(cellValue)) return false;
        break;
      }
      case 'WILDCARD': {
        const wildcardRegex = new RegExp(
          `^${token.value.replace(/\*/g, '.*').replace(/\?/g, '.')}$`,
          'i'
        );
        if (!wildcardRegex.test(cellValue)) return false;
        break;
      }
      case 'NUMERIC_RANGE': {
        const numericValue = parseFloat(cellValue);
        const { lower, upper } = token.range!;
        if (numericValue < parseFloat(lower) || numericValue > parseFloat(upper)) return false;
        break;
      }
      case 'DATE_RANGE': {
        const dateValue = new Date(cellValue).getTime();
        const { lower, upper } = token.range!;
        const lowerDate = new Date(lower).getTime();
        const upperDate = new Date(upper).getTime();
        if (dateValue < lowerDate || dateValue > upperDate) return false;
        break;
      }
      default:
        break;
    }
  }

  return true;
}

/**
 * The main custom search filter for per-column filtering.
 */
export const googleSearchFilter: FilterFn<any> = (
  row: Row<any>,
  columnId: string,
  filterValue: string
) => {
  if (!filterValue) return true; // Show all rows if no filter value

  // Parse the query into tokens
  const tokens = parseSearchQuery(filterValue);

  // Get the cell value for the current column
  const cellValue = String(row.getValue(columnId) ?? '');

  // Evaluate the tokens against the cell value
  return evaluateTokens(tokens, cellValue);
};
