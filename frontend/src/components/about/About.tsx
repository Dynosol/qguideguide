// About.tsx
import React, { useEffect } from 'react';
import '/src/assets/css/About.css';
import ViewColumnIcon from '@mui/icons-material/ViewColumn';
import SearchIcon from '@mui/icons-material/Search';
import SwapVertIcon from '@mui/icons-material/SwapVert';

const About: React.FC = () => {
  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      const cards = document.getElementsByClassName('card') as HTMLCollectionOf<HTMLElement>;
      Array.from(cards).forEach(card => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        card.style.setProperty('--mouse-x', `${x}px`);
        card.style.setProperty('--mouse-y', `${y}px`);
      });
    };

    const cardsContainer = document.getElementById('cards');
    if (cardsContainer) {
      cardsContainer.addEventListener('mousemove', handleMouseMove);
    }

    return () => {
      if (cardsContainer) {
        cardsContainer.removeEventListener('mousemove', handleMouseMove);
      }
    };
  }, []);

  return (
    <div className="about min-h-screen transition-colors duration-300 flex flex-col items-center justify-center py-12 pt-20">
      <div className="container mx-auto px-4">
        {/* Header */}
        <div className="text-center">
          <h1 className="text-5xl md:text-6xl lg:text-7xl font-semibold text-gray-800 dark:text-gray-100 mb-10">
            About the QGuideGuide
          </h1>
          <div className="mb-16">
            <p className="text-base md:text-lg text-gray-600 dark:text-gray-300">
              <i>This tool was created because it's hard to compare courses to each other and against themselves across semesters in the official QGuide. This is a faster tool to search the QGuide, filter by any metric, and compare courses based on historical data (currently supports Fall 2019 - Spring 2023)</i>
            </p>
          </div>
        </div>

        {/* Grid of Cards */}
        <div id="cards" className="flex flex-wrap gap-3 justify-center relative">
          {[
            {
              title: 'Methodology',
              subtitle: (<>
              All data is scraped from the official QGuide. Nothing is tampered with, and no data is removed or added unless otherwise stated.
              The Professor Scores, along with the rest of the QGuideGuide are purely a representation of the information that is already available to Harvard Students in the QReports,
              publicly avilable through Bluera, and publicly available through several other sources.
              None of the information on the QGuideGuide reflects the opinions or beliefs of its creators.
              It also does not reflect any extra evaluation put upon any courses or instructors.
              It is merely a re-representation to filter and compare information already available to students.
              All of the information here is possible to individually and manually access through the QReports.
              </>)
            },
            {
              title: 'Rankings Explained',
              subtitle: (<>
              <b style={{ color: "var(--harvard)"}}>We believed comparing course ratings via naive average was not the best way </b>
              <i>(i.e. a course with 3 responses with a 5 average vs. a course with 79 responses with a 4.97 average) </i>
              The "weighted rankings" are calculated via an empirical bayesian estimation with a normal distribution prior, which is all from the QGuide data.
              The prior is calculated separately for all courses and all courses within a department (sums and sums of squares for variance).
              We assume variance decreases with observations, so observed variance is the reciprocal of number of responses.
              Finally, the Empirical Bayes score is obtained by linearly combining the observed mean and the prior mean using the shrinkage weight.
              The values we calculate should be repeatable by any scrapist, with minor variation due to how the rare missing/invalid/funky data is handled.
              <b> In other words, the rating gains confidence the more ratings there are. </b>
              If you're confused, take Stat110.
              </>)
            },
            {
              title: 'Letter Gradings Explained',
              subtitle: (<>
              The letters represent purely a percentile range in the weighted data, not quality or an evaluation external from the publicly accessible QGuide data.
              The ranges for [S+, S, S-, A+, A, A-, B+, B, B-, C, D, F] are calculated if they surpass a certain percentile: [0.1, 0.5, 1, 2, 5, 10, 20, 40, 60, 80, 95, 100].
              For example, if the weighted score for a course's materials is in the 47th percentile, it would receive a B-. A course with a weighted score in 61st percentile gets a C.
              These letters exist purely for easy comparison and are not meant to be taken as a "grade" or "evaluation" of the course, other than how past students have filled out the QGuide.
              They exist so that you can eyeball the data and see how a courses' score compares, since a number like 4.32 has little intuitive meaning.
              Unfortunately, there is no grade inflation here.
              </>)
            },
            { 
              title: 'Professor Scores Explained',
              subtitle: (<>
              Treat this page with a grain of salt. "Total Ratings" stands for the number of individual QGuide responses for any course that instructor has ever taught.
              "Rating" is a weighted score compared to all other instructors that have ever taught a course (in the data range) on the "Evaluate your Instructor overall." question (once again, treat the specific "ratings" with a grain of salt).
              "Department Score" represents the weighted scores 
              </>)
            },
            {
              title: 'How to Use the Course Search',
              subtitle: (<>
              (Press <ViewColumnIcon /> to view more columns!!)
              The <SearchIcon /> [Search all Fields] searches across all columns.
              Text-input column filters have "google-eqsue" functions, i.e. "COMPSCI 50" will limit course titles to ONLY COMPSCI 50.
              The most powerful tool (and why this was created) is the sort <SwapVertIcon /> function,
              which you can change on the top dropdown menu to sort by ratings that are calcuated via empirical bayesian weighted scores, empirical bayesian scores weighted across the department, or by just the raw averages of the scores.
              </>)
            },
            {
              title: 'Why? And Who?',
              subtitle: (<>
              The QGuideGuide was created because it's really annoying to navigate the QGuide (searching each course up manually?)
              For example, if you want to look for a list of courses within a specific department, you might not be able see them all next to each other (QGuide pages are limited).
              Also, even if you can, you can't compare their QScores, unless you open a ton of tabs and flip through them back and forth (which we've done many times before).
              You might be able to view courses by department in my.harvard, but then you can't see the QScores!
              The most powerful tools in the QGuideGuide are course search, filtering on specific attributes, viewing more columns, and professor scores.
              </>)
            },
            {
              title: 'Upcoming features',
              subtitle: (<>
              Here's a rough list of features that may more may not be added in the future, depending on interest and time.
              More historical data (Fall 2024, as soon as it comes out).
              Weighted rating support for the "Recommend to other students" question.
              <b> User input to supplement data (i.e. you could input grade distributions, comments, etc. would involve logins). </b>
              Pages for individual courses that display changes over time, user input, etc.
              Mobile support.
              </>)
            },
            {
              title: 'Contact',
              subtitle: (
                <>
                  Found a bug? Want a new feature? Have an issue? Want to join the team? Reach out via{' '}
                  <a href="mailto:contact@qguideguide.com" style={{ color: "var(--harvard)", textDecoration: 'underline' }}>
                    contact@qguideguide.com
                  </a>.
                </>
              )
            }
          ].map((card, index) => (
            <div
              key={index}
              className="
                card 
                bg-white dark:bg-gray-800 
                rounded-lg 
                relative 
                min-h-[200px]
                transition-colors duration-300
                border border-gray-400 dark:border-transparent
                shadow-xl
                flex
                flex-col
              "
            >
              <div className="
                card-content 
                bg-white dark:bg-zinc-900
                rounded-lg 
                p-6 
                flex 
                flex-col 
                gap-4
                text-center
                transition-transform duration-300
                h-full
              ">
                <h3 className="text-gray-800 dark:text-gray-100 text-xl font-semibold">
                  {card.title}
                </h3>
                <div className="text-base text-gray-600 dark:text-gray-300">
                  {card.subtitle}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default About;
