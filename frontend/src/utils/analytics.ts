import ReactGA from 'react-ga4';

// Initialize Google Analytics
export const initGA = (trackingId: string) => {
  if (typeof window !== 'undefined') {
    ReactGA.initialize(trackingId);
  }
};

// Track page views
export const pageView = (path: string) => {
  if (typeof window !== 'undefined') {
    ReactGA.send({ hitType: 'pageview', page: path });
    console.log(`Logged page view for: ${path}`);
  }
};

// Track events
export const event = ({ 
  category, 
  action, 
  label, 
  value 
}: { 
  category: string, 
  action: string, 
  label?: string, 
  value?: number 
}) => {
  if (typeof window !== 'undefined') {
    ReactGA.event({
      category,
      action,
      label,
      value
    });
  }
};

// Track user timing
export const timing = ({
  category,
  variable,
  value,
  label
}: {
  category: string,
  variable: string,
  value: number,
  label?: string
}) => {
  if (typeof window !== 'undefined') {
    ReactGA.send({
      hitType: 'timing',
      timingCategory: category,
      timingVar: variable,
      timingValue: value,
      timingLabel: label
    });
  }
}; 