from dotenv import load_dotenv
import os
load_dotenv()

def calculate_similarity(user_answer, ideal_answer):
    if not user_answer or not ideal_answer:
        return 0.0
        
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
        
    documents = [user_answer, ideal_answer]
    vectorizer = TfidfVectorizer().fit_transform(documents)
    vectors = vectorizer.toarray()
    
    similarity = cosine_similarity([vectors[0]], [vectors[1]])[0][0]
    return float(similarity * 100)

def generate_technical_feedback(score):
    if score >= 80:
        return "Excellent! You have a strong grasp of this concept."
    elif score >= 50:
        return "Good effort, but you could be more specific with technical terms."
    else:
        return "You need to review the core concepts of this topic. Try explaining with examples next time."

import os
import json
import traceback

LOCAL_IDEAL_ANSWERS = {
    # Python (English)
    "What are decorators in Python and why are they used?": 
        "Decorators in Python are wrapper functions that modify the behavior of another function without changing its source code. They are commonly used for logging, authorization, caching, and measuring execution time.",
    "Explain the difference between list and tuple with use cases.":
        "Lists are mutable sequences defined with square brackets [], meaning they can be modified. Tuples are immutable sequences defined with parentheses (), meaning they cannot be changed and are faster and safer for read-only data.",
    "What is PEP 8 and why is it important?":
        "PEP 8 is the official style guide for writing Python code. It ensures code readability, consistency, and clean formatting across projects.",
    "How is memory managed in Python? Explain Garbage Collection.":
        "Memory in Python is managed automatically using private heap space and reference counting. When an object's reference count drops to zero, it is deleted. The Garbage Collector also finds and removes cyclic references.",
    "What are generators and how do they differ from iterators?":
        "Generators are a simple way to create iterators using the 'yield' keyword to return values lazily one-by-one. Unlike standard iterators, they do not store the entire sequence in memory, making them highly efficient.",
    "Explain the concept of GIL (Global Interpreter Lock).":
        "The GIL is a mutex in CPython that prevents multiple native threads from executing Python bytecodes at once. It ensures thread-safe memory management but limits CPU-bound multi-threaded execution.",
        
    # Django (English)
    "What is the MVT pattern in Django? How is it different from MVC?":
        "Django uses the Model-View-Template (MVT) pattern. Unlike MVC where the Controller handles routing, Django's View acts as the controller, and templates act as the view layer to render output.",
    "Explain Django Middleware and its lifecycle.":
        "Middleware is a framework of hooks that process requests and responses globally. In its lifecycle, a request passes through middleware sequentially before reaching the view, and the response passes back in reverse order.",
    "What are signals in Django? Give a real-world example.":
        "Signals allow decoupled applications to get notified when certain events occur. For example, a post_save signal can trigger sending a welcome email immediately after a new user profile is created in the database.",
    "How do you handle database migrations in Django?":
        "Migrations are Django's way of propagating changes you make to your models into your database schema. They are created using 'makemigrations' and applied using the 'migrate' command.",
    "Explain the role of Django Rest Framework (DRF) in building APIs.":
        "DRF is a powerful toolkit for building Web APIs in Django. It provides serialization to convert models to JSON, built-in authentication, request routing, and a web-browsable API shell.",
    "How do you handle authentication in Django projects?":
        "Django has a built-in authentication system that handles user accounts, groups, permissions, and sessions. For APIs, token-based (like JWT) or session-based authentication via DRF is commonly used.",

    # SQL (English)
    "Difference between INNER JOIN, LEFT JOIN, and RIGHT JOIN.":
        "INNER JOIN returns records that have matching values in both tables. LEFT JOIN returns all records from the left table and matched records from the right table. RIGHT JOIN returns all records from the right table and matched records from the left.",
    "Explain Database Normalization (1NF, 2NF, 3NF).":
        "Normalization organizes database columns and tables to reduce redundancy. 1NF removes duplicate columns; 2NF ensures all non-key columns depend on the primary key; 3NF removes transitive dependencies.",
    "What are Primary Keys, Foreign Keys, and Unique Keys?":
        "A Primary Key uniquely identifies each row in a table and cannot be null. A Foreign Key references a primary key in another table to maintain relationships. A Unique Key ensures distinct values in a column.",
    "How do you optimize a slow SQL query?":
        "Slow queries can be optimized by adding indexes to frequently filtered/joined columns, avoiding SELECT *, using EXPLAIN to analyze the execution plan, and rewriting subqueries as joins.",
    "What is an Index in SQL and how does it improve performance?":
        "An Index is a database structure that allows fast lookup of rows in a table. It works like a book index, avoiding full table scans and significantly reducing query execution time.",
    "Explain the ACID properties in database transactions.":
        "ACID stands for Atomicity (all or nothing), Consistency (preserves database rules), Isolation (independent concurrent transactions), and Durability (permanent saved changes even after system crash).",
        
    # React (English)
    "What are Hooks in React? Explain useEffect.":
        "Hooks let functional components use state and other React features. The useEffect hook allows performing side effects like data fetching, subscription, or manual DOM updates in functional components.",
    "Difference between Functional and Class components.":
        "Functional components are JavaScript functions that accept props and return JSX, using Hooks for state management. Class components are ES6 classes that extend React.Component and use lifecycle methods.",
    "What is Virtual DOM and how does it work?":
        "The Virtual DOM is a lightweight, in-memory representation of the real DOM. When state changes, React updates the virtual DOM, compares it with the previous version (diffing), and updates only the changed parts in the real DOM (reconciliation).",
    "Explain State vs Props in React.":
        "State is a local, mutable data storage that is managed within the component itself. Props are immutable read-only parameters passed down from a parent component to a child component.",
    "How do you handle API calls in a React application?":
        "API calls in React are typically handled inside the useEffect hook using fetch or axios, and the fetched data is then stored in the component's state using useState.",
    "What is Redux and when should we use it?":
        "Redux is a state management library for global application state. It should be used in large-scale applications where state needs to be shared across many deeply nested or unrelated components.",

    # Java (English)
    "Explain the concept of OOPs in Java.":
        "Java OOPs concepts include inheritance (reusing code), polymorphism (methods doing different things), abstraction (hiding internal details), and encapsulation (binding data and methods together securely).",
    "Difference between Abstract Class and Interface.":
        "An abstract class can have instance variables and both concrete and abstract methods. An interface can only have public static final variables and (traditionally) only abstract methods, supporting multiple inheritance.",
    "What is Spring Boot and why is it popular?":
        "Spring Boot is a Java framework that simplifies spring application development. It is popular because of auto-configuration, starter dependencies, built-in embedded servers (Tomcat), and rapid project bootstrap.",
    "Explain Exception Handling in Java.":
        "Exception handling in Java prevents system crash using try, catch, finally, throw, and throws. It ensures graceful recovery and normal program execution flow during runtime errors.",
    "What is Hibernate and how does it relate to ORM?":
        "Hibernate is a popular Java framework that implements Object-Relational Mapping (ORM). It maps Java object classes directly to database tables, reducing JDBC boilerplate code.",
    "Explain Multithreading in Java.":
        "Multithreading in Java allows concurrent execution of two or more parts of a program for maximum CPU utilization. It is achieved by extending the Thread class or implementing the Runnable interface.",

    # HR (English)
    "Tell me about yourself and your background.":
        "A strong answer should briefly summarize your professional background, highlight your key technical skills, mention recent projects, and explain why you are interested in this position.",
    "Why should we hire you for this role?":
        "A strong answer should connect your skills directly to the job description, highlight your problem-solving abilities, and express your passion to add value to the team.",
    "What are your greatest strengths and weaknesses?":
        "A strong answer should highlight 2-3 genuine professional strengths (e.g. fast learner, team player) and a real but non-critical weakness along with the active steps you are taking to improve it.",
    "Where do you see yourself in the next 5 years?":
        "A strong answer should show career growth, ambition to master the technology stack, desire to take on leadership responsibilities, and long-term commitment to the company.",
    "How do you handle conflict in a team environment?":
        "A strong answer should describe listening to all sides, remaining calm and objective, focusing on the root problem rather than personal differences, and working collaboratively towards a win-win solution.",
    "Tell me about a time you faced a difficult challenge at work/college.":
        "A strong answer should follow the STAR method: describe the Situation, the Task at hand, the Action you took to resolve it, and the positive Result achieved.",

    # Python (Tanglish)
    "Python-ல Decorators-னா என்ன, அது ஏன் use பண்றாங்க?":
        "Python-ல Decorators-னா ஒரு function-ஓட behavior-ஐ modify பண்ண யூஸ் பண்ற wrapper functions. Code-ஐ மாத்தாமலேயே logging, caching, authentication-லாம் add பண்ண இத யூஸ் பண்ணுவாங்க.",
    "List-க்கும் Tuple-க்கும் இருக்குற difference-ஐ examples-ஓட explain பண்ணுங்க.":
        "List-னா mutable (modify பண்ணலாம்), [] square brackets-ல define பண்ணுவோம். Tuple-னா immutable (modify பண்ண முடியாது), () parentheses-ல define பண்ணுவோம்; இது list-ஐ விட fast-ஆ இருக்கும்.",
    "PEP 8-ன்னா என்ன? அது ஏன் important?":
        "PEP 8-ன்றது Python code எழுதுறதுக்கான official style guide. Code consistency, readability-ஐ maintain பண்ணவும், மத்தவங்க code-ஐ ஈஸியா புரிஞ்சுக்கவும் இது ரொம்ப important.",
    "Python-ல memory management எப்படி நடக்குது? Garbage Collection பத்தி சொல்லுங்க.":
        "Python-ல private heap space மற்றும் reference counting மூலமா memory manage ஆகுது. ஒரு object-ஓட reference 0 ஆகும்போது, Garbage Collector அத auto-வா clean பண்ணிடும்.",
    "Generators-னா என்ன? அது iterators-ல இருந்து எப்படி differ ஆகுது?":
        "Generators-னா 'yield' keyword யூஸ் பண்ணி values-ஐ lazily (ஒவ்வொன்னா) return பண்ற functions. இது memory-ல எல்லா values-ஐயும் store பண்ணாம run ஆகுறதால iterator-ஐ விட fast-ஆ இருக்கும்.",
    "GIL (Global Interpreter Lock) concept-ஐ explain பண்ணுங்க.":
        "GIL-ன்றது CPython compiler-ல இருக்குற mutex. இது ஒரே நேரத்துல ஒரு thread-ஐ மட்டும் தான் run பண்ண அனுமதிக்கும்; memory management safe-ஆ இருக்க இது யூஸ் ஆகுது.",

    # Django (Tanglish)
    "Django-ல MVT pattern-னா என்ன? இது MVC-ல இருந்து எப்படி different?":
        "Django MVT (Model-View-Template) pattern-ஐ யூஸ் பண்ணுது. MVC-ல Controller பண்ற routing வேலையை Django-ல View பண்ணுது, Template-ன்றது user rendering-க்கு template files-ஐ வச்சுக்குது.",
    "Django Middleware மற்றும் அதோட lifecycle பத்தி சொல்லுங்க.":
        "Middleware-ன்றது Django request & response-ஐ globally process பண்ற hooks. Request view-க்கு போறதுக்கு முன்னாடியும், response user-க்கு போறதுக்கு முன்னாடியும் middleware வழியா தான் பாஸ் ஆகும்.",
    "Django-ல Signals-னா என்ன? ஒரு real-world example குடுங்க.":
        "Signals-னா decoupled apps-க்கு நடுவுல event triggers-ஐ handle பண்ணும். Example: ஒரு User profile create ஆனதும் automatic-ஆ welcome mail சென்ட் பண்ண post_save signal யூஸ் பண்ணலாம்.",
    "Django migrations-ஐ எப்படி handle பண்ணுவீங்க?":
        "Models-ல பண்ற changes-ஐ database schema-ல update பண்ண migrations யூஸ் ஆகுது. 'makemigrations' மூலமா migration files create பண்ணி, 'migrate' command வச்சு database-ல update பண்ணுவோம்.",
    "APIs build பண்ணும்போது Django Rest Framework (DRF)-ஓட role என்ன?":
        "DRF-ன்றது Django-ல REST APIs-ஐ fast-ஆ build பண்ண யூஸ் ஆகுற toolkit. இது serializing, auth configuration, model viewsets-லாம் easy-ஆ provide பண்ணுது.",
    "Django projects-ல authentication-ஐ எப்படி handle பண்ணுவீங்க?":
        "Django-வோட built-in auth system வச்சு session & user permissions handle பண்ணலாம். APIs-க்கு token-based auth (JWT tokens) DRF மூலமா integrate பண்ணலாம்.",

    # SQL (Tanglish)
    "INNER JOIN, LEFT JOIN மற்றும் RIGHT JOIN difference என்ன?":
        "INNER JOIN ரெண்டு table-லையும் match ஆகுற rows-ஐ மட்டும் தரும். LEFT JOIN left table-ல இருக்குற எல்லா rows மற்றும் right table matching rows-ஐ தரும். RIGHT JOIN right table rows மற்றும் left table matching rows-ஐ தரும்.",
    "Database Normalization (1NF, 2NF, 3NF) பத்தி explain பண்ணுங்க.":
        "Database normalization-ன்றது data redundancy-ஐ குறைச்சு table-ஐ organize பண்றது. 1NF-ல duplicate rows இருக்காது, 2NF-ல partial dependency இருக்காது, 3NF-ல transitive dependency இருக்காது.",
    "Primary Keys மற்றும் Foreign Keys-னா என்ன?":
        "Primary Key-ன்றது ஒரு table-ல இருக்குற row-ஐ uniquely identify பண்ணும் (cannot be NULL). Foreign Key-ன்றது இன்னொரு table-ல இருக்குற primary key-ஐ refer பண்ணி relationship-ஐ maintain பண்ணும்.",
    "ஒரு slow SQL query-ஐ எப்படி optimize பண்ணுவீங்க?":
        "Query optimization-க்கு columns-ல indexing பண்ணலாம், selective column names மட்டும் SELECT பண்ணனும், EXPLAIN query plan செக் பண்ணி subqueries-க்கு பதிலா joins யூஸ் பண்ணலாம்.",
    "SQL-ல Index-னா என்ன? அது performance-ஐ எப்படி improve பண்ணுது?":
        "Index-ன்றது database search performance-ஐ fast-ஆக்க யூஸ் ஆகுற lookup structure. Full table scan பண்ணாம, book index-ல தேடுற மாதிரி query-ஐ ரொம்ப fast-ஆக்கும்.",
    "Database transactions-ல ACID properties-ஐ explain பண்ணுங்க.":
        "ACID-னா Atomicity (முழுசா நடக்கணும் இல்லனா நடக்காது), Consistency (rules follow பண்ணும்), Isolation (transactions தனித்தனியா நடக்கும்), மற்றும் Durability (data permanent-ஆ database-ல சேவ் ஆகும்).",

    # React (Tanglish)
    "React Hooks-னா என்ன? useEffect பத்தி explain பண்ணுங்க.":
        "Functional components-ல state மற்றும் lifecycle features-ஐ யூஸ் பண்ண Hooks உதவுது. useEffect Hook-ன்றது data fetching, side-effects மற்றும் manual DOM updates-ஐ handle பண்ண யூஸ் ஆகுது.",
    "Functional மற்றும் Class components-க்கு இருக்குற difference என்ன?":
        "Functional component-ன்றது props-ஐ accept பண்ணி JSX-ஐ return பண்ற simple JavaScript function. Class component ES6 class extends பண்ணி lifecycle methods வச்சு run ஆகுற complex class.",
    "Virtual DOM-னா என்ன? அது எப்படி work ஆகுது?":
        "Virtual DOM-ன்றது browser DOM-ஓட lightweight memory copy. State change ஆகும்போது React virtual DOM-ஐ update பண்ணி, diffing pattern மூலமா changes-ஐ மட்டும் real DOM-ல update பண்ணும்.",
    "React-ல State vs Props difference சொல்லுங்க.":
        "State-ன்றது component-க்குள்ளயே manage ஆகுற mutable data (change பண்ணலாம்). Props-ன்றது parent component-ல இருந்து child component-க்கு pass ஆகுற read-only immutable data.",
    "React app-ல API calls எப்படி handle பண்ணுவீங்க?":
        "React-ல API calls-ஐ useEffect Hook-குள்ள fetch() method அல்லது axios library யூஸ் பண்ணி call பண்ணுவோம்; அப்புறம் useState state variable-ல data-ஐ store பண்ணுவோம்.",
    "Redux-னா என்ன? அதை எப்போ use பண்ணனும்?":
        "Redux-ன்றது application state-ஐ global-ஆ ஒரே இடத்துல store பண்ணி manage பண்ற tool. component tree ரொம்ப பெருசா இருக்கும்போதும், state sharing complex-ஆ இருக்கும்போதும் இத யூஸ் பண்ணனும்.",

    # Java (Tanglish)
    "Java-ல OOPs concepts-ஐ explain பண்ணுங்க.":
        "Java OOPs concepts core features: Inheritance (reusing code), Polymorphism (overloading/overriding methods), Abstraction (hiding details), and Encapsisation (data protection).",
    "Abstract Class-க்கும் Interface-க்கும் இருக்குற difference என்ன?":
        "Abstract class-ல instance variables மற்றும் abstract/concrete methods ரெண்டும் இருக்கலாம். Interface-ல abstract methods மற்றும் public static final constants மட்டும் தான் இருக்க முடியும்.",
    "Spring Boot ஏன் இவ்ளோ popular-ஆ இருக்கு?":
        "Spring Boot-ல auto-configuration, rapid development support, embedded servers (Tomcat) மற்றும் code boilerplate-ஐ குறைக்கிறதால Java developers-க்கு இது ரொம்ப popular-ஆ இருக்கு.",
    "Java-ல Exception Handling பத்தி explain பண்ணுங்க.":
        "Exception handling-ன்றது run-time errors-ல இருந்து program crash ஆகாம தடுக்கிறது. Java-ல try, catch, finally, throw, throws-ஐ வச்சு exceptions handle பண்ணுவோம்.",
    "Hibernate-னா என்ன? அது ORM-கூட எப்படி relate ஆகுது?":
        "Hibernate-ன்றது Java model class-ஐ database table-கூட map பண்ற Object-Relational Mapping (ORM) framework. இது database queries writing boilerplates-ஐ குறைக்கும்.",
    "Java multithreading பத்தி சொல்லுங்க.":
        "ஒரே நேரத்துல Multiple threads-ஐ run பண்ணி program process speed-ஐ maximum-ஆக்குறது. Runnable interface அல்லது Thread class-ஐ extend பண்ணி Java-ல multithreading பண்ணலாம்.",

    # HR (Tanglish)
    "உங்கள பத்தியும் உங்க background பத்தியும் சொல்லுங்க.":
        "உங்க answer-ல உங்க professional overview, projects, key technical skills மற்றும் இந்த role மேல இருக்குற interest-ஐ பத்தி simple-ஆ சொல்லணும்.",
    "நாங்க ஏன் உங்கள இந்த role-க்கு hire பண்ணனும்?":
        "உங்க technical skills இந்த job description-க்கு எப்படி match ஆகுது, உங்க problem solving skills மற்றும் team success-க்கு எப்படி contribute பண்ணுவீங்கனு explain பண்ணனும்.",
    "உங்க strengths மற்றும் weaknesses என்ன?":
        "உங்க real professional strengths (fast learner, team player) மற்றும் ஒரு non-critical weakness-ஐ சொல்லி அத நீங்க எப்படி improve பண்ணிட்டு இருக்கீங்கனு positive-ஆ சொல்லணும்.",
    "Next 5 years-ல உங்கள எங்க பாக்குறீங்க?":
        "உங்க career-ல next level technical growth, leadership skills, புதிய technologies கத்துக்கிறது மற்றும் company growth-க்கு support பண்ற மாதிரி long-term commitment சொல்லணும்.",
    "ஒரு team environment-ல conflicts-ஐ எப்படி handle பண்ணுவீங்க?":
        "எல்லாரோட opinion-ஐயும் அமைதியா கேட்டு புரிஞ்சுக்குவேன், root problem-ஐ solve பண்ண focused-ஆ பேசி, team harmony maintain பண்ற மாதிரி resolution கொண்டு வருவேன்.",
    "உங்க career-ல நீங்க face பண்ண ஒரு difficult challenge பத்தி சொல்லுங்க.":
        "STAR method follow பண்ணனும்: Challenge situation என்ன, task என்ன, நீங்க என்ன actions எடுத்து solve பண்ணீங்க மற்றும் அதனால கிடைச்ச positive result/output என்னனு சொல்லணும்.",

    # Tamil (ta-IN)
    "பைத்தானில் டெக்கரேட்டர்கள் (Decorators) என்றால் என்ன, அவை ஏன் பயன்படுத்தப்படுகின்றன?":
        "டெக்கரேட்டர்கள் என்பது ஒரு சார்பின் (Function) குறியீட்டை மாற்றாமல் அதன் செயல்பாட்டை மாற்றியமைக்கும் அமைப்பாகும். இவை பொதுவாக லாகிங், கேச்சிங் மற்றும் அங்கீகாரத்திற்குப் பயன்படுத்தப்படுகின்றன.",
    "List மற்றும் Tuple இடையிலான வித்தியாசத்தை தகுந்த உதாரணங்களுடன் விளக்குங்கள்.":
        "List என்பது மாற்றக்கூடியது (Mutable), சதுர அடைப்புக்குறிகளுடன் [] வரையறுக்கப்படுகிறது. Tuple என்பது மாற்ற முடியாதது (Immutable), அடைப்புக்குறிகளுடன் () வரையறுக்கப்படுகிறது.",
    "PEP 8 என்றால் என்ன மற்றும் அது ஏன் முக்கியமானது?":
        "PEP 8 என்பது பைதான் குறியீடு எழுதுவதற்கான அதிகாரப்பூர்வ பாணி வழிகாட்டி (Style Guide). இது குறியீட்டின் வாசிப்புத்திறன் மற்றும் சீரான தன்மையை உறுதி செய்ய உதவுகிறது.",
    "பைத்தானில் மெமரி மேனேஜ்மென்ட் எப்படி செய்யப்படுகிறது? கார்பேஜ் கலெக்ஷன் (Garbage Collection) பற்றி விளக்குங்கள்.":
        "பைத்தானில் மெமரி மேனேஜ்மென்ட் தானியங்கி குறிப்பு எண்ணல் (Reference Counting) மூலம் செய்யப்படுகிறது. ஒரு பொருளின் குறிப்பு பூஜ்ஜியமாகும்போது கார்பேஜ் கலெக்டர் அதை நீக்குகிறது.",
    "Generators என்றால் என்ன மற்றும் அவை Iterators-லிருந்து எப்படி வேறுபடுகின்றன?":
        "Generators என்பது 'yield' முக்கிய வார்த்தையைப் பயன்படுத்தி மதிப்புகளை ஒவ்வொன்றாக வழங்கும் எளிய சார்புகள் ஆகும். இவை முழு பட்டியலையும் நினைவகத்தில் சேமிக்காது.",
    "GIL (Global Interpreter Lock) என்ற கருத்தை விளக்குங்கள்.":
        "CPython-ல் ஒரு நேரத்தில் ஒரு த்ரெட் (Thread) மட்டுமே பைதான் பைட்கோடை இயக்க முடியும் என்பதை உறுதி செய்யும் மியூடெக்ஸ் (Mutex) ஆகும்.",
    "Django-வில் MVT பேட்டர்ன் என்றால் என்ன? இது MVC-யிலிருந்து எப்படி வேறுபடுகிறது?":
        "Django மாடல்-வியூ-டெம்ப்ளேட் (MVT) முறையைப் பயன்படுத்துகிறது. MVC-ல் கன்ட்ரோலர் செய்யும் ரூட்டிங் பணிகளை Django-வில் வியூ (View) செய்கிறது.",
    "Django Middleware மற்றும் அதன் வாழ்க்கைச் சுழற்சி (Lifecycle) பற்றி விளக்குங்கள்.":
        "Middleware என்பது கோரிக்கைகள் (Requests) மற்றும் பதில்களை (Responses) செயலாக்கும் உலகளாவிய கொக்கிகள் (Hooks) ஆகும். கோரிக்கை வியூவை அடையும் முன் மிடில்வேர் வழியாகச் செல்லும்.",
    "Django-வில் Signals என்றால் என்ன? ஒரு நிஜ கால உதாரணத்தைக் கூறுங்கள்.":
        "இரண்டு வெவ்வேறு பயன்பாடுகள் நிகழ்வுகள் மூலம் தொடர்புகொள்ள சிக்னல்கள் உதவுகின்றன. எடுத்துக்காட்டாக, புதிய பயனர் கணக்கு உருவாக்கப்பட்டவுடன் தானியங்கி மின்னஞ்சல் அனுப்புதல்.",
    "Django-வில் டேட்டாபேஸ் மைக்ரேஷன்களை (Migrations) எப்படி கையாள்வீர்கள்?":
        "மாடல்களில் செய்யும் மாற்றங்களை டேட்டாபேஸ் ஸ்கீமாவில் புதுப்பிக்க மைக்ரேஷன்கள் பயன்படுகின்றன. 'makemigrations' மற்றும் 'migrate' கட்டளைகள் மூலம் இது செய்யப்படுகிறது.",
    "API-களை உருவாக்குவதில் Django Rest Framework (DRF)-ன் பங்கு என்ன?":
        "DRF என்பது Django-வில் REST API-களை எளிதாகவும் வேகமாகவும் உருவாக்க உதவும் ஒரு சிறந்த டூல்கிட் (Toolkit) ஆகும். இது சீரியலைசேஷன், அங்கீகாரம் போன்றவற்றை வழங்குகிறது.",
    "Django புராஜெக்ட்களில் அத்தென்டிகேஷன் (Authentication) முறையை எப்படி கையாள்வீர்கள்?":
        "Django-வின் உள்ளமைக்கப்பட்ட அங்கீகார அமைப்பைப் பயன்படுத்தலாம். API-களுக்கு டோக்கன் அடிப்படையிலான அங்கீகாரம் (JWT) DRF மூலம் ஒருங்கிணைக்கப்படுகிறது.",
    "INNER JOIN, LEFT JOIN மற்றும் RIGHT JOIN இடையிலான வித்தியாசம் என்ன?":
        "INNER JOIN இரு அட்டவணைகளிலும் பொருந்தும் வரிசைகளை மட்டும் தரும். LEFT JOIN இடது அட்டவணையின் அனைத்து வரிசைகளையும் தரும். RIGHT JOIN வலது அட்டவணையின் அனைத்து வரிசைகளையும் தரும்.",
    "டேட்டாபேஸ் நார்மலைசேஷன் (1NF, 2NF, 3NF) பற்றி விளக்குங்கள்.":
        "நார்மலைசேஷன் என்பது தரவு தேக்கத்தைக் குறைக்கும் முறை. 1NF நகல் நெடுவரிசைகளை நீக்குகிறது, 2NF பகுதி சார்புகளை நீக்குகிறது, 3NF பரிமாற்ற சார்புகளை நீக்குகிறது.",
    "Primary Keys, Foreign Keys மற்றும் Unique Keys என்றால் என்ன?":
        "Primary Key என்பது அட்டவணையில் ஒரு வரிசையை தனித்துவமாக அடையாளம் காட்டும். Foreign Key என்பது மற்றொரு அட்டவணையின் பிரைமரி கீயைக் குறிக்கும்.",
    "SQL Query-ஐ எப்படி ஆப்டிமைஸ் செய்வது?":
        "அடிக்கடி தேடப்படும் நெடுவரிசைகளுக்கு இண்டெக்ஸ் (Index) உருவாக்குதல், தேவையான நெடுவரிசைகளை மட்டும் தேர்ந்தெடுத்தல் மற்றும் EXPLAIN பயன்படுத்தி பகுப்பாய்வு செய்தல்.",
    "SQL-ல் Index என்றால் என்ன மற்றும் அது செயல்திறனை (Performance) எப்படி மேம்படுத்துகிறது?":
        "இண்டெக்ஸ் என்பது அட்டவணையில் தரவைத் தேடும் வேகத்தை அதிகரிக்கும் ஒரு தேடல் அமைப்பு. இது முழு அட்டவணையையும் தேடாமல் விரைவாகத் தேட உதவுகிறது.",
    "டேட்டாபேஸ் டிரான்சாக்ஷன்களில் ACID பண்புகளை விளக்குங்கள்.":
        "ACID என்பது அணுத்தன்மை (Atomicity), நிலைத்தன்மை (Consistency), தனிமைப்படுத்தல் (Isolation) மற்றும் நீடித்து நிலைத்தல் (Durability) ஆகும்.",
    "React-ல் Hooks என்றால் என்ன? useEffect பற்றி விளக்குங்கள்.":
        "Hooks என்பது செயல்பாட்டு கூறுகளில் (Functional Components) நிலை மற்றும் பிற அம்சங்களைப் பயன்படுத்த உதவுகிறது. useEffect பக்க விளைவுகளைக் கையாள்கிறது.",
    "Functional மற்றும் Class கூறுகளுக்கு (Components) இடையிலான வித்தியாசம் என்ன?":
        "Functional Component என்பது எளிய ஜாவாஸ்கிரிப்ட் சார்பு. Class Component என்பது ES6 கிளாஸ் மற்றும் லைஃப்சைக்கிள் முறைகளைக் கொண்ட சிக்கலான அமைப்பு.",
    "Virtual DOM என்றால் என்ன மற்றும் அது எப்படி வேலை செய்கிறது?":
        "Virtual DOM என்பது உண்மையான DOM-ன் நினைவக நகலாகும். மாற்றங்கள் ஏற்படும் போது React இரண்டையும் ஒப்பிட்டு, தேவையான மாற்றங்களை மட்டும் உண்மையான DOM-ல் புதுப்பிக்கும்.",
    "React-ல் State மற்றும் Props இடையிலான வித்தியாசத்தை விளக்குங்கள்.":
        "State என்பது ஒரு கூறுக்குள்ளேயே நிர்வகிக்கப்படும் மாற்றக்கூடிய தரவு. Props என்பது பெற்றோர் கூறிலிருந்து குழந்தைக்கு அனுப்பப்படும் மாற்ற முடியாத தரவு.",
    "React அப்ளிகேஷனில் API கால்களை (Calls) எப்படி கையாள்வீர்கள்?":
        "React-ல் API கால்கள் பொதுவாக useEffect கொக்கிக்குள் fetch() அல்லது axios பயன்படுத்தி அழைக்கப்பட்டு, useState-ல் சேமிக்கப்படுகின்றன.",
    "Redux என்றால் என்ன மற்றும் அதை எப்போது பயன்படுத்த வேண்டும்?":
        "Redux என்பது பயன்பாட்டின் ஒட்டுமொத்த நிலையையும் ஒரே இடத்தில் சேமித்து நிர்வகிக்கும் நூலகம் ஆகும். பெரிய மற்றும் சிக்கலான பயன்பாடுகளில் இதைப் பயன்படுத்தலாம்.",
    "ஜாவாவில் OOPs என்ற கருத்தை விளக்குங்கள்.":
        "ஜாவாவின் OOPs கோட்பாடுகள்: மரபுரிமம் (Inheritance), பல்லுருவாக்கம் (Polymorphism), சுருக்கம் (Abstraction) மற்றும் உறைபொதியாக்கம் (Encapsulation).",
    "Abstract Class மற்றும் Interface இடையிலான வித்தியாசம் என்ன?":
        "Abstract Class-ல் மாறிகள் மற்றும் நடைமுறைப்படுத்தப்பட்ட முறைகள் இருக்கலாம். Interface-ல் மாறிலிகள் மற்றும் செயல்படுத்தப்படாத முறைகள் மட்டுமே இருக்க முடியும்.",
    "Spring Boot என்றால் என்ன மற்றும் அது ஏன் பிரபலமானது?":
        "Spring Boot என்பது ஸ்பிரிங் பயன்பாடுகளை எளிதாக உருவாக்க உதவும் ஒரு ஜாவா கட்டமைப்பாகும். இது தானியங்கி கட்டமைப்பு மற்றும் எளிய உருவாக்கத்தை வழங்குகிறது.",
    "ஜாவாவில் எக்ஸெப்ஷன் ஹேண்ட்லிங் (Exception Handling) பற்றி விளக்குங்கள்.":
        "இயக்க நேர பிழைகளால் நிரல் முடங்குவதைத் தடுக்கும் முறை. இது try, catch, finally, throw, throws மூலம் கையாளப்படுகிறது.",
    "Hibernate என்றால் என்ன மற்றும் அது ORM-உடன் எப்படி தொடர்புடையது?":
        "Hibernate என்பது ஜாவா வகுப்புகளை டேட்டாபேஸ் அட்டவணைகளுடன் இணைக்கும் ஒரு ORM கட்டமைப்பு ஆகும். இது குறியீட்டு தேக்கத்தைக் குறைக்கிறது.",
    "ஜாவாவில் மல்டித்ரெடிங் (Multithreading) பற்றி விளக்குங்கள்.":
        "ஒரே நேரத்தில் பல பணிகளை இயக்கி செயலியின் திறனை அதிகப்படுத்துதல். இது Thread கிளாஸ் அல்லது Runnable இடைமுகம் மூலம் செய்யப்படுகிறது.",
    "உங்களைப் பற்றியும் உங்கள் பின்னணியைப் பற்றியும் சொல்லுங்கள்.":
        "உங்கள் பணி பின்னணி, தொழில்நுட்ப திறன்கள், சமீபத்திய திட்டங்கள் மற்றும் இந்த வேலை மீதான ஆர்வம் ஆகியவற்றை சுருக்கமாக கூற வேண்டும்.",
    "நாங்கள் ஏன் உங்களை இந்த வேலைக்கு அமர்த்த வேண்டும்?":
        "உங்களின் தொழில்நுட்ப திறன்கள் இந்த வேலைக்கு எவ்வாறு பொருந்துகிறது மற்றும் நிறுவனத்தின் வளர்ச்சிக்கு நீங்கள் எவ்வாறு பங்களிக்க முடியும் என்பதை கூற வேண்டும்.",
    "உங்கள் பலம் மற்றும் பலவீனங்கள் என்ன?":
        "உங்களின் நேர்மறையான தொழில்முறை பலங்களையும், பாதிப்பில்லாத ஒரு பலவீனத்தையும் கூறி, அதை எவ்வாறு சரிசெய்து வருகிறீர்கள் என்பதை விளக்க வேண்டும்.",
    "அடுத்த 5 ஆண்டுகளில் உங்களை எங்கே பார்க்கிறீர்கள்?":
        "தொழில்நுட்பத்தில் சிறந்த வளர்ச்சி, புதிய பொறுப்புகளை ஏற்று நடத்துதல் மற்றும் நிறுவனத்துடன் நீண்ட காலம் பயணிக்கும் அர்ப்பணிப்பை வெளிப்படுத்த வேண்டும்.",
    "ஒரு குழு சூழலில் நீங்கள் மோதல்களை (Conflicts) எப்படி கையாள்வீர்கள்?":
        "அனைவரின் கருத்துக்களையும் கேட்டு,root பிரச்சனையை கண்டறிந்து, குழுவின் ஒற்றுமையை சீர்குலைக்காமல் சுமுகமான தீர்வு காண முயற்சிப்பேன்.",
    "வேலையில் அல்லது கல்லூரியில் நீங்கள் சந்தித்த ஒரு கடினமான சவாலைப் பற்றி சொல்லுங்கள்.":
        "சவால் என்ன, அதை தீர்க்க நீங்கள் எடுத்த முயற்சிகள் மற்றும் அதன் மூலம் கிடைத்த நேர்மறையான முடிவுகளை STAR முறையில் விளக்க வேண்டும்."
}

def basic_evaluate_session(session):
    total_score = 0
    questions = session.questions.all()
    
    for q in questions:
        q_text = q.question_text.strip()
        ideal = None
        
        # Look up ideal answer locally
        for key, val in LOCAL_IDEAL_ANSWERS.items():
            if key.lower() in q_text.lower() or q_text.lower() in key.lower():
                ideal = val
                break
                
        if not ideal:
            ideal = f"A proper answer for '{q.question_text}' should cover its core definition, practical use cases, and why it is important in real-world scenarios."
            
        q.score = calculate_similarity(q.user_answer, ideal)
        q.ideal_answer = ideal
        q.feedback = generate_technical_feedback(q.score)
        q.save()
        total_score += q.score
        
    session.score = total_score / len(questions) if questions else 0
    session.save()
    return session.score

def evaluate_session(session):
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    questions = session.questions.all()
    
    if not questions:
        session.score = 0
        session.save()
        return 0

    if not api_key:
        return basic_evaluate_session(session)
        
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        qa_list = []
        for q in questions:
            qa_list.append({
                "id": q.id,
                "question": q.question_text,
                "user_answer": q.user_answer or "No answer provided"
            })
            
        prompt = f"""
        You are an expert technical interviewer evaluating a candidate's responses.
        Here are the questions asked and the candidate's answers:
        {json.dumps(qa_list, indent=2)}
        
        For each question, provide:
        1. "score": A score out of 100 based on the accuracy and completeness of the candidate's answer. Give 0 if they didn't answer.
        2. "ideal_answer": A concise, accurate, and ideal answer to the question (around 2-3 sentences).
        3. "feedback": Constructive feedback on their answer. Tell them what they missed or what was good.
        
        If the language of the session ({session.language}) is 'ta-EN' (Tanglish), you MUST provide both the 'ideal_answer' and 'feedback' in Tanglish (Tamil language written using the English/Latin alphabet, keeping technical terms in English but writing the connecting words and sentence structure in Tamil using English/Latin alphabet).
        If the language of the session ({session.language}) is 'ta-IN' (Tamil), you MUST provide both the 'ideal_answer' and 'feedback' in formal Tamil script.
        If the language of the session ({session.language}) is 'en-US' (English), you MUST provide both the 'ideal_answer' and 'feedback' in English.
        
        Return the result as a JSON array of objects, where each object has:
        "id" (integer, matching the input id), "score" (integer), "ideal_answer" (string), "feedback" (string).
        """
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        elif response_text.startswith('```'):
            response_text = response_text[3:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
            
        result_data = json.loads(response_text.strip())
        
        total_score = 0
        result_map = {item["id"]: item for item in result_data}
        
        for q in questions:
            if q.id in result_map:
                eval_data = result_map[q.id]
                q.score = float(eval_data.get("score", 0))
                q.ideal_answer = eval_data.get("ideal_answer", "")
                q.feedback = eval_data.get("feedback", "")
            else:
                q.score = 0
                q.ideal_answer = "Could not generate ideal answer."
                q.feedback = "Could not evaluate."
                
            q.save()
            total_score += q.score
            
        session.score = total_score / len(questions)
        session.save()
        return session.score
        
    except Exception as e:
        tb = traceback.format_exc()
        try:
            with open("scratch/evaluation_error.log", "w") as f:
                f.write(f"Exception in evaluate_session:\n{tb}\n")
        except:
            pass
        print(f"AI Evaluation failed: {e}")
        traceback.print_exc()
        return basic_evaluate_session(session)
