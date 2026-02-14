Hugging Face transformers:
- Expects us to create virtual environments etc., and has version compability problems.
  - In our scenario, we do not solve version compability problems and use only ecosystem drivers.
- Downloading models:
  - Sometimes you wait days for licence.
  - Download page lacks the scenario to understand in 5 seconds, that this is a model and there is a button to install it;
    - Inclusively, it does not give you list of standard models, which work.

This break all our policies:
- No version conflicts, but autoresolution
- Standard model lists
- Command line tools and/or graphical user interface
- Python compability
  - It has it theoretically, but over 5 minutes of installation means our 20 libraries take 1 hour and 40 minutes minimal,
    - which is not suitable because: any bug, error or discomfort accumulates and creates unexpected leaks.

Superior examples for us - Quick Basic, Turbo Pascal, Borland Pascal:
- Single, reliable installer.
- No understanding for it's internals. We do not run them on ethical basis.
- Offline documentation.
- Standard examples.
- Backwards-compability. We do not want 2 years old books look like talking of another library.
- Offline models, software, offline run
  - Online support is plus

For the real world and it's complexity, nearly each library, driver or system we describe breaks *some* of those, and I do not mind
specific personal preferrences of it's creators; but if we take this easily:
- We are not serving users, but creating lifelong dependency.
- We are not creating software, but users are working on our packaging problems
  - and creating something out of it.

For example, my code examples can be installed and run.

Hugging Face is still used by general things given here - but those systems install it on their own, and manage all the model complexity:
- In this case, you install that specific system and use it's built-in model list, but not directly the hugging face library.

I want to teach AI, I am not interested in general problems of programming, management and the feeling that everything can run online, and python should be virtualized:
- Rather, Python is superior language, which needs package management:
  - Running files on __main__ == __self__, on their own in subfolders needs separate include folders and is tough problem.
  - Python's package manager cannot easily install alt. packages and resolve problems; instead developers expect you often to have several folders with complete sets of libraries
  - Installed software often duplicates it all instead of running standard python - because it cannot act along with the packaged installations
 
Out of this trouble, we then use toolkits, which are able to install their own python, manage all the packages, and altough it's a stupid waste of space in an ideal world;
- For our practical purpose, we *do not want to work on software administration*, but rather we use graphical tools, cli and python scripting.
- Many people live in enlightened world, where internet won't break and they are not offline;
  - For an average american, they won't believe you would do any effort for car, credit card, mobile and always-online life cycle.
  - They show it's extreme comfort if you do not have download button for most of their package;
    - or if you need to build downloaded docs.

Policy here:
- We accept, if good library has only online docs, but it's not a *feature*: it's definite bug.
  - Standard library creators acceptably, *do not* invent anything in particular about my computer or lifestyle - this is packaging and administrative bug of *expecting lifestyles*, not even software.
  - For example, you can download my documentations for offline use in one click, and you can see it's not harder to read with complexity of these few buttons or links or features.
- We use online models for their efficiency, but we *always* create an offline environment.
  - Without this, we cannot even create online environments on our own.
- We want to see installers and packaged software.
  - Indeed, this for standardization:
    - For experimentation, we are especially interested in things like small models, which need git clone, build and install.

I am a hacker in this sense to break all the policies and get something out of real world, but any installation-time problems or temporal unavilability of software, models or docs: I take this with serious caution.
- For example, even if I am 100% online, I do not want 10 minute or 20 minute break in documentation access and especially:
  - I am not very interested in comfort levels of typical american - I am sure you can watch good online TV, but typically I fail if I cannot do this with my own computer and especially, I do not trust people who
    show me certain "comfort level" of not adding any support of non-american life style - for example, a single phone card outdated of mine, and I did not have access to several old accounts; the google system
    ensured efficient hacker protection, but it turned out I am rather a hacker without permanent phone card - I stopped favouring google products, because *nothing really happened with this failure*.
