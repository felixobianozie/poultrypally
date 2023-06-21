## PoultryPally 💡
PoultryPally is a digital assistant with a complete set of tools for small & medium scale poultry farm management.   

It is a free digital product for the everyday farmer. The ✨magic✨ in this app is just incredible!  

It is strictly designed with simplicity in mind to help the next door farmer keep track of everything about his bird livestock.  

This product has the simplest learning curve and is your best choice.  

PoultryPally is constantly improving with more features being added on a regular basis.  

## The Inspiration 🌤️
In my [(Felix Obianozie)](felixobianozie@gmail.com) demographic, there are more poultry farmers than there are of any other livestock. On the fateful day, my nextdoor neigbour who has a bird farm expressed some frustration over not getting the right tool to manage her farm. "...they either are just too complex and overpriced or too simple to fit my needs as a small/medium scale everyday farmer." Those were her exact words when I inquired about the already existing tools. I thought, "a Software Engineer is a problem solver right?" That thought led to something, which led to another, and here we are with this spectacular product...</smiles>.

**NB:** *PoultryPally is a miniature version of [**FarmPally**]() a larger, premium, full featured farm management tool by thesame author*

## Features 😮
- Keep an inventory of farm items
- Organise farm records in batches (a collection of livestock stocked by the farmer at thesame time and assumed to be of same age and similar size).
- Track production costs within farm
- Track sales of farm produce
- Document customer details and purchase activities
- Keep mortality records and automatically reconcile it with production cost
- Auto suggest selling price based on a given constraints
- Track fram profits and losses
- Many more great features on the way...

## Production 🚀
This product is available for free public use at the following link: [PoultryPally App Link]()
**NB**: *In the event of a downtime or inaccessibility, please try again later.*

## Run Locally 🏃
Want to install and run the app locally on your machine? Let's do it then!

 **1.   Clone the project**
 ```
git clone <project_link>
```  

 **2.   Confirm that Python 3+ is installed on your machine.**
  ```
  python --version
  ```  

 **NB:** 
 If Python is installed, you should see a message like “Python 3.x.x”. Note that “3.x.x” represents the version number of Python. Proceed to the next section (3).
 
 If Python 3+ is not installed, install it using the following [GUIDE](https://www.tutorialsteacher.com/python/install-python). After installation, join me at the next section (3).

 
 **3.   Setup a virtual environment**
  **NB:** *On mac or ubuntu, change all "python" to "python3" and "pip" to "pip3" and you will be fine.*

 **Install virtualenv** *(a tool for creating python virtual env with ease)*
  ```
  python -m pip install virtualenv
  ```
  **Create virtual environment**
  ```
  virtualenv venv
  ``` 
 
  Where "venv" is my preferred name for the virtual environment. You may change it to whatever fits for you.  
  
  **NB:** There are other ways of creating virtual environments in Python, checkout this [GUIDE](https://www.geeksforgeeks.org/create-virtual-environment-using-venv-python/)

  **Activate the virtual environment**
  ```
  venv\scripts\activate
  ```
  
  Where "venv" remains the name of your virtual machine as specified during the creation stage.
  
  If your got here successfully, then we are in for the sweeter stuff, getting the app to run!🥂
  
   **4. Install All App Dependencies**
  ```
  pip install -r requirements.txt
  ```

  **5. Perform Django Data Migration**
   ```
  python manage.py makemigrations
  python manage.py migrate
  ```
  **NB:** This step performs all the needed connection and database setups between the application models, Django ORM and the database.
  The open source version of this project is configured to SQL Lite by default, but runs MySQL in production. To switch to a different database, refer to this [GUIDE]()

   **6. Start The App Server**
   ```
  python manage.py runserver
  ```
  **NB:** This runs the app on localhost:8080 by default.
  
  Get to your favourite browser, and enjoy the goodness of PoultryPally on: http://127.0.0.1:8000/. Am glad you made it😃! Enjoy!

## Tech 💻
**NB**: *PoultryPally is currently Server Side Rendered (SSR), hence there is a little overlap of frontend and backend tech. That said, I will just list them all.*
| Trademark | Description |
| ------ | ------ |
| [![](https://i.imgur.com/4l6Eeh3.jpg)]() | [Python](https://www.python.org/) - a topnotch language of the present and the future ideal for app developpment and analysis 💕|
| [![](https://i.imgur.com/Lpv3HnM.png)]() | [Django](https://www.djangoproject.com/) - high-level Python web framework that encourages rapid development and clean, pragmatic design|
| [![](https://i.imgur.com/YqaIv6O.png)]() | [Javascript](https://www.javascript.com/) - one of the best things that happened in the world of programming languages...😉 |
| [![](https://i.imgur.com/nek6z1Q.jpg)]() | [Tailwind](https://tailwindcss.com/) -  utility-first CSS framework for rapidly building modern websites without ever leaving your HTML |
| [![](https://i.imgur.com/Mce5kDC.png)]() | [MySQL](https://www.mysql.com/) - open-source relational database management system |
| [![](https://i.imgur.com/AByWAOv.png)]() | [Boostrap]() - great UI boilerplate and CSS framework for modern web apps |


## Models 🧱
Below is a snapshot of the current model. Care for a complete copy in a portable format? Shoot me a request @ [felixobianozie@gmail.com]()

![image](https://i.imgur.com/Qak0Kw0.pngg)
![image](https://i.imgur.com/Cyt4BRf.png)
![image](https://i.imgur.com/LoFMjei.png)
![image](https://i.imgur.com/0tCZS8I.png)

## Developers ✒️
- [Felix Obianozie](felixobianozie@gmail.com) - Lead Developer (UI/UX Design, Frontend, Backend, Devops & Maintenance)
- [Nathaniel Efe Oghene]() - Contributor (UI/UX Design)
- More contributors are welcome...