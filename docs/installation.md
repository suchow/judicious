---
layout: page
title: Installation
---

Install the Judicious client using `pip`:

```
pip install judicious
```

To run your own Judicious server, ...


## Configuration
You will need to set the following environment variables.

<table>
  <tbody>
    <tr>
      <td><code>JUDICIOUS_RECRUITER</code></td>
      <td>The recruiter used to procure judicious participants.
      Currently, only <code>MTurkRecruiter</code> is available.</td>
    </tr>
    <tr>
      <td><code>JUDICIOUS_REDUNDANCY</code></td>
      <td>The number of times that each task should be completed. The canonical
      result is the first completed result. A positive integer.</td>
    </tr>
    <tr>
      <td><code>AWS_ACCESS_KEY_ID</code></td>
      <td>An access key ID for Amazon Mechanical Turk.</td>
    </tr>
    <tr>
      <td><code>AWS_SECRET_ACCESS_KEY</code></td>
      <td>A secret access key for Amazon Mechanical Turk</td>
    </tr>
    <tr>
      <td><code>AWS_DEFAULT_REGION</code></td>
      <td>The default AWS region. <code>us-east-1</code> is a good default.</td>
    </tr>
    <tr>
      <td><code>JUDICIOUS_MTURK_MODE</code></td>
      <td>Where to run MTurk HITs: <code>live</code> or <code>sandbox</code>.</td>
    </tr>
    <tr>
      <td><code>JUDICIOUS_MTURK_HIT_TYPE_ID_SANDBOX</code></td>
      <td>When running on the MTurk sandbox, what HIT Type should the HIT be registered under?</td>
    </tr>
    <tr>
      <td><code>JUDICIOUS_MTURK_HIT_TYPE_ID_LIVE</code></td>
      <td>When running on live MTurk, what HIT Type should the HIT be registered under?</td>
    </tr>
    <tr>
      <td><code>JUDICIOUS_SECRET_KEY</code></td>
      <td>A secret key for signing browser cookies.</td>
    </tr>
    <tr>
      <td><code>JUDICIOUS_MTURK_LIFETIME</code></td>
      <td>How long, in seconds, between a HIT being posted and it being removed from MTurk.</td>
    </tr>
    <tr>
      <td><code>JUDICIOUS_TASK_TIMEOUT</code></td>
      <td>How long, in seconds, between a task being started and it being returned to the queue.</td>
    </tr>
    <tr>
      <td><code>JUDICIOUS_LOG_LEVEL</code></td>
      <td>How verbose the Judicious client should be: <code>debug</code>, <code>info</code>, <code>warning</code>, or <code>error</code>.</td>
    </tr>
    <tr>
      <td><code>RECAPTCHA_SECRET_KEY</code></td>
      <td>Secret key for Google Recaptcha.</td>
    </tr>
    <tr>
    <td><code>RECAPTCHA_SITE_KEY</code></td>
    <td>Site key for Google Recaptcha.</td>
    </tr>
  </tbody>
</table>
