import React from 'react';

const Contact: React.FC = () => (
    <div className="contact-containe non-navbar">
      <h1 className="contact-title">Contact Me</h1>
      <p className="contact-description">
          Let me know if there's any bugs or if you just want to say hi
      </p>
      
      <form method="post">
          <div className="form-group">
              <input
                  type="text"
                  name="name"
                  className="form-control"
                  placeholder="Your Name"
                  required
                  id="id_name"
              />
          </div>
          <div className="form-group">
              <input
                  type="email"
                  name="email"
                  className="form-control"
                  placeholder="Your Email"
                  required
                  id="id_email"
              />
          </div>
          <div className="form-group">
              <textarea
                  name="message"
                  className="form-control"
                  rows={5}
                  placeholder="Your Message"
                  required
                  id="id_message"
              ></textarea>
          </div>
          <div className="form-group">
              {/* {{ form.captcha }} */}
          </div>
          <div className="form-submit">
              <button type="submit" className="btn-submit">Send Message</button>
          </div>
      </form>
      {/* Messages Section */}
      {/* {% if messages %}
      {% for message in messages %}
      <div class="alert-message" role="alert">
          {{ message }}
      </div>
      {% endfor %}
      {% endif %} */}
  </div>
);

export default Contact;
