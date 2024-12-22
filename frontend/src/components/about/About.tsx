import React from 'react';

const About: React.FC = () => (
    <div className="container mt-5 mb-5">
        <div className="row justify-content-center">
            <div className="col-lg-8 col-md-10 col-sm-12">
                <h1>About QGuideGuide</h1>
                <p>
                    Welcome to QGuideGuide! Our platform helps students make informed decisions about their courses
                    by providing comprehensive professor rankings and course reviews.
                </p>

                <h2>Our Mission</h2>
                <p>
                    Our mission is to empower students with reliable information to help them achieve their academic
                    goals. We believe in transparency, collaboration, and student success.
                </p>

                <h2>Features</h2>
                <ul>
                    <li>Detailed professor rankings based on student feedback.</li>
                    <li>Comprehensive course reviews and recommendations.</li>
                    <li>A user-friendly platform for accessing and sharing academic insights.</li>
                </ul>

                <h2>Contact Us</h2>
                <p>
                    Have questions or feedback? We'd love to hear from you! Reach out to us at{' '}
                    <a href="mailto:support@qguideguide.com">support@qguideguide.com</a>.
                </p>
            </div>
        </div>
    </div>
);

export default About;
