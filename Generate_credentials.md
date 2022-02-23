# How generate `credentials.json`

First of all, go to [Google Cloud Console](https://console.cloud.google.com/) and create a new project.

![stage 1](.github/assets/generate_credentials/1.png)

Chose a name for your project and click on `Create` button.

![stage 2](.github/assets/generate_credentials/2.png)

Then, go to `OAuth consent screen`, chose `external` user type and click on `Create` button.

![stage 3](.github/assets/generate_credentials/3.png)

Fill out `Application name`, `User support email` and `Developer email address` and click on `Save and continue` button 3 times and finally click on `Back to dashboard` button.

![stage 4](.github/assets/generate_credentials/4.png)

Then, we need to allow `Google Calendar API` to access your google account. Select `Library` tab.

![stage 5](.github/assets/generate_credentials/5.png)

Search for `Google Calendar API` and select it.

![stage 6](.github/assets/generate_credentials/6.png)

After that, click on `Enable` button.

![stage 7](.github/assets/generate_credentials/7.png)

Now, you can generate your `credentials.json` file. Select `Credentials` tab and click on `Create credentials` button and choose `OAuth client ID`.

![stage 8](.github/assets/generate_credentials/8.png)

Select `Desktop app` as `Application type`, fill out `Application name` and click on `Create` button.

![stage 9](.github/assets/generate_credentials/9.png)

Then, download your generated credentials file.

![stage 10](.github/assets/generate_credentials/10.png)
