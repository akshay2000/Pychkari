# Pychkari

[![Build Status](https://travis-ci.com/akshay2000/Pychkari.svg?branch=master)](https://travis-ci.com/akshay2000/Pychkari)

A Very Simple Python Dependency Injector

## Installation

Use pip!

    pip install pychkari


## Overview

Pychkari (pronounced peach kaa ree) is a simple dependency injector for Python. It is intended to be a no-fuss library that depends on as few packages as possible and just works.

This example should get us started!

    # Class definitions for reference
    
    class A:
        def __init__(self, 
                     depOne,                    # casing support
                     second_dep: "DepTwo",      # annotations support
                     const_dep=3):              # not a dependency
            self.dep1 = depOne
            self.dep2 = second_dep
            self.const_d = const_dep
        
        
    class DepOne:
        def __init__(self):
            self.timestamp = datetime.now()
    
    
    class DepTwo:
        def __init__(self):
            self.timestamp = datetime.now()
    
    
    class B:
        def __init__(self, a, dep_one):
            self.a = a
            self.dep1 = dep_one
            
            
    # registration
    
    container = Container.instance()
    container.register("MyAwesomeService", B)   # explicitly named registration
    container.register_class(A)                 # service name "A" implicit
    container.register_class(DepOne)            # service name "DepOne" implicit
    container.register_class(DepTwo)            # service name "DepTwo" implicit
    
    # instantiation
    
    service = container.get("MyAwesomeService") # creates instance of "B" with dependencies injected


## Features

### Lightweight

Pychkari is barely a few kilobytes. It doesn't have third party dependencies. Just drop it into your project and run with it.

### Zero Commitment

Pychkari doesn't require you to change your code. As long as common Python conventions are followed, your existing code just works!  
No fancy annotations, no decorations, no commitments. You're free to mix and match with any other framework.

This chart should tell you how dependencies are resolved:

| Dependency            | Resolved Service Name |
|-----------------------|-----------------------|
| underscore_case       | UnderscoreCase        |
| camelCase             | CamelCase             |
| PascalCase            | PascalCase            |
| my_Weird_case         | MyWeirdCase           |
| my_service:HttpClient | HttpClient            |

### Extensible

Well, sort of! If the conventions don't satisfy your complex naming schemes, you can always make the names explicit by annotating the dependencies.  
For example, `client:"MyService"` will inject and instance of `MyService` in place of `client`.

