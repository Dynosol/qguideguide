import React from 'react';

const Contact: React.FC = () => (
    <div className="container">
        <div className="row justify-content-center">
            <div className="col-lg-8 col-md-10 col-sm-12">
                <div className="card shadow-lg border-0 rounded-4">
                    <div className="card-body p-5">
                        <h1 className="card-title text-center mb-4">Contact Me</h1>
                        <p className="text-center">Let me know if there's any bugs or if you just want
                            to say hi</p>
                        <form method="post">
                            <div className="mb-3">
                                <input type="text" name="name" className="form-control rounded-3" placeholder="Your Name"
                                    required id="id_name">
                                </input>
                            </div>
                            <div className="mb-3">
                                <input type="email" name="email" className="form-control rounded-3" placeholder="Your Email"
                                    required id="id_email">
                                </input>
                            </div>
                            <div className="mb-3">
                                <textarea name="message" className="form-control rounded-3" rows={5} placeholder="Your Message"
                                    required id="id_message"></textarea>
                            </div>
                            <div className="mb-3">
                                {/* {{ form.captcha }} */}
                            </div>

                            <div className="text-center">
                                <button type="submit" className="btn btn-dark mt-3 px-5 rounded-3">Send Message</button>
                            </div>
                        </form>

                        {/* {% if messages %}
                        {% for message in messages %} */}
                        {/* <div class="alert alert-success mt-4 rounded-3" role="alert">
                            {{ message }}
                        </div>
                        {% endfor %}
                        {% endif %} */}
                    </div>
                </div>
            </div>
        </div>
    </div>
);

export default Contact;