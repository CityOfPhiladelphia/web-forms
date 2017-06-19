# Web Forms

Simple service to handle unauthenticated web forms, like contact us and feedback.

### Usage

A submission takes the form of:

```sh
POST /forms/beta-feedback/submissions
Host: https://webforms.phila.gov
Content-Type: application/json
Content-Length: 138

{
    "recaptcha": "somerandomslug",
    "what_happened": "I have a suggestion or idea.",
    "tell_us_more": "Have more pictures of puppies."
}
```

`beta-feedback` is a form that is registered in the web form database. `recaptcha` is the response token from Google ReCAPTCHA and is verified against Google to prevent SPAM and abuse. The rest of the JSON data is saved as the form submission.

Google Invisible ReCAPTCHA can be used, which verifies a user in the background without requiring them to solve something.

### Form Config

Example:

```sh
{
    "name": "my-form",
    "title": "My Form",
    "description": "A form to submit things about me",
    "action": "webhook",
    "schema": null,
    "action_config": {
    	"url": "https://foo.com/webhook"
    },
    "max_submissions_per_minute": 5,
    "created_at": "2017-06-19T09:56:44.888144+00:00",
    "updated_at": "2017-06-19T09:56:44.888144+00:00"
}
```

`action` can be:

- `store_only` - Just store the submission in the database.
- `google_sheets` - Publish the form submission to a Google Sheet.
- `webhook` - POST the submission data to a URL.
- `taskflow_task` - Queue a [Taskflow](https://github.com/CityOfPhiladelphia/taskflow) task.
- `taskflow_workflow` - Queue a [Taskflow](https://github.com/CityOfPhiladelphia/taskflow) workflow.

Configuration options, such as `url` for `webhook`, is stored in the `action_config` object.
