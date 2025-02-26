# Media Content Management System with User Authentication

A simple and modern web application built using **Flask** and **Socket.IO** to manage media files (images and videos). The application features user authentication, media file upload, viewing, and deletion, all with a beautiful, responsive **Material Design** interface.

---

## Features

- **User Authentication**: Log in with a predefined username and password (no database required for authentication).
- **Media Upload**: Upload images (`.jpg`, `.jpeg`) and videos (`.mp4`) to the server.
- **Media Display**: View uploaded media files in a responsive, Material Design grid layout.
- **Media Deletion**: Delete uploaded media files directly from the interface.
- **Responsive Design**: Fully responsive layout for mobile, tablet, and desktop views.
- **Socket.IO Integration**: Real-time updates for media upload and deletion events.


---

## Demo

Yet to Upload this


---

## Repos:
1. Git Repo 1: https://github.com/DotDev-Sudo/dashboard_v2
2. Docker Image: https://hub.docker.com/r/sanjaykshebbar/dashboard_v2

---
## More Information and comparison of this tool:

https://docs.google.com/document/d/1kKM8m7qLkr5Qdq7YP_EUZ8ehRRQx9t87wViwPuE8dRE/edit?tab=t.0

## Detailed Documentation can be found here!!
https://docs.google.com/document/d/1llskI_pduFzKKmNElugKcvaIfTrzwn_D44rDwqAzC58/edit?tab=t.tti7clkfkvd4


## Technologies Used

- **Flask**: Lightweight Python web framework for routing, session management, and serving HTML templates.
- **Socket.IO**: Real-time communication between the server and client for media upload and deletion events.
- **HTML & CSS**: Frontend technologies used for creating the structure and styling the application.
- **Material Design Lite (MDL)**: A CSS and JS library to style the app with Google's Material Design principles.
- **SQLite **: A lightweight database for storing user data with encrypted password.

---

## Prerequisites

Before setting up the project, ensure that you have the following installed on your machine:

#### 1. A Linux, Windows or Mac Machine

#### 2. Containerization Application
You need one of the following containerization applications installed:

- **Docker CLI** (preferred)
- **Podman**
- **Rancher**

#### Installing Docker:
If you're using Docker, you can follow the official installation guide for your distribution:
- [Docker Installation Guide](https://docs.docker.com/get-docker/)

#### Installing Podman:
If you're using Podman, you can follow the official installation guide:
- [Podman Installation Guide](https://podman.io/getting-started/installation)

#### Installing Rancher:
If you're using Rancher, follow the official installation guide:
- [Rancher Installation Guide](https://rancher.com/docs/rancher/v2.5/en/installation/)


## How to Run the Project

### Prerequisites
Before running the project, ensure that the following prerequisites are fulfilled:
1. A **Linux, Windows or Mac machine** with a containerization application like Docker, Podman, or Rancher.
2. Docker is recommended for this setup.

If Docker is not installed, please follow the instructions in the **Prerequisites** section to install Docker or another containerization application.

### Steps to Run the Application

1. **Open the terminal** on your Linux machine.

2. **Run the following Docker command** to start the container with the application:

    ```bash
    docker run -d --network="bridge" -p 5000:5000 sanjaykshebbar/dashboard_v2:v2
    ```

    #### Explanation of the Docker command:

    - `docker run`: This command runs a container from a specified image.
    - `-d`: This flag runs the container in the background (detached mode).
    - `--network="bridge"`: This specifies the network mode for the container. The `bridge` network is a default network in Docker, ensuring that the container can communicate with other containers on the same network.
    - `-p 5000:5000`: This flag maps the host machine's port 5000 to the container's port 5000, making the application accessible on port 5000 of your host machine.
    - `sanjaykshebbar/dashboard_v2:v2`: This is the name of the Docker image being used. It's a versioned image (`v2`), and this image contains the application code.

3. **Access the application**:
    - Once the container is running, you can access the application via a web browser.
    - Open a browser and enter the following URL to access the app:
    
    ```plaintext
    http://<IP/Hostname>:5000
    ```
    
    This will launch the blank page of the application.

4. **Access the Management Dashboard**:
    - To access the media management dashboard, navigate to the login page:
    
    ```plaintext
    http://<IP/Hostname>:5000/login
    ```
    
    - Enter the following credentials to log in: (This is the defaut user, where this can be removed / Modified later.)
      - **Username**: `Admin`
      - **Password**: `Password@123`

**Note:** Here the user name is case sensitive too.
    After logging in, you will have access to the **media management dashboard**. Here, you can manage the media content, which includes adding or removing media files (MP4 videos and JPG images).

---

### Managing Media:
Once logged in, you can:
- **Upload media**: Add new MP4 or JPG files to the media library.
- **Delete media**: Remove existing media files from the system.

### NOTE:
- This tool will automatically fetches the updated media content and get that displayed, where there is no manual intervention needed here.
- This tool doesnot need internet if hosting in an Isolated environment.
- In simple words this tool works as a wireless pendrive where the data (Images and Videos) will be shared over the local network to a remote display.
- This tool will save the data inside that container itself under the path /media, and based on the media management the data can be manuplated. (Removal and Addition)
