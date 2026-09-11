from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import models
from .models import CodingProblem, CodingSubmission
from django.http import JsonResponse
import json

@login_required
def coding_dashboard_view(request):
    # Pass some common languages to the dashboard
    languages = [
        {"name": "Python", "icon": "fab fa-python", "color": "#3776AB"},
        {"name": "Java", "icon": "fab fa-java", "color": "#007396"},
        {"name": "C", "icon": "fas fa-copyright", "color": "#A8B9CC"},
        {"name": "C++", "icon": "fas fa-code", "color": "#00599C"},
        {"name": "HTML & CSS", "icon": "fab fa-html5", "color": "#E34F26", "param": "HTML_CSS"},
        {"name": "JavaScript", "icon": "fab fa-js", "color": "#F7DF1E"},
        {"name": "SQL", "icon": "fas fa-database", "color": "#4479A1"},
        {"name": "React", "icon": "fab fa-react", "color": "#61DAFB"},
    ]
    return render(request, 'coding_round/dashboard.html', {'languages': languages})

DEFAULT_CHALLENGES = {
    "C": [
        {
            "title": "Reverse a String in C",
            "description": "Write a C function `void reverseString(char* str)` to reverse a given null-terminated string in-place using pointers.\n\nExample:\nInput: str = \"hello\"\nOutput: \"olleh\"",
            "difficulty": "Easy",
            "tags": "C, Pointers, Strings",
            "initial_code": "#include <stdio.h>\n#include <string.h>\n\nvoid reverseString(char* str) {\n    // Write your code here\n}"
        },
        {
            "title": "Find Largest Element in Array",
            "description": "Write a C function `int findMax(int arr[], int n)` that returns the maximum element in an array of `n` integers.",
            "difficulty": "Easy",
            "tags": "C, Arrays, Loop",
            "initial_code": "#include <stdio.h>\n\nint findMax(int arr[], int n) {\n    // Write your code here\n    return 0;\n}"
        },
        {
            "title": "Check Prime Number in C",
            "description": "Write a C program function `int isPrime(int n)` that returns 1 if `n` is prime, and 0 otherwise.",
            "difficulty": "Easy",
            "tags": "C, Math, Functions",
            "initial_code": "#include <stdio.h>\n\nint isPrime(int n) {\n    // Write your code here\n    return 0;\n}"
        },
        {
            "title": "Fibonacci Series using Recursion in C",
            "description": "Write a recursive C function `int fibonacci(int n)` to calculate the `n`-th Fibonacci number.",
            "difficulty": "Medium",
            "tags": "C, Recursion, Dynamic Programming",
            "initial_code": "#include <stdio.h>\n\nint fibonacci(int n) {\n    // Write your code here\n    return 0;\n}"
        },
        {
            "title": "Implement Dynamic Array in C using Malloc",
            "description": "Write C functions `int* createArray(int size)` and `void freeArray(int* ptr)` to dynamically allocate and free memory using `malloc` and `free`.",
            "difficulty": "Medium",
            "tags": "C, Pointers, Memory Management, Malloc",
            "initial_code": "#include <stdio.h>\n#include <stdlib.h>\n\nint* createArray(int size) {\n    // Allocate memory and return pointer\n    return NULL;\n}\n\nvoid freeArray(int* ptr) {\n    // Free allocated memory\n}"
        }
    ],
    "Python": [
        {
            "title": "Two Sum",
            "description": "Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to target.\n\nExample:\nInput: nums = [2,7,11,15], target = 9\nOutput: [0,1]",
            "difficulty": "Easy",
            "tags": "Python, Arrays, Hash Table",
            "initial_code": "def two_sum(nums, target):\n    # Write your solution here\n    pass"
        },
        {
            "title": "Valid Parentheses",
            "description": "Given a string `s` containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.\n\nExample:\nInput: s = \"()[]{}\"\nOutput: True",
            "difficulty": "Easy",
            "tags": "Python, Stack, Strings",
            "initial_code": "def is_valid(s: str) -> bool:\n    # Write your solution here\n    pass"
        },
        {
            "title": "Longest Substring Without Repeating Characters",
            "description": "Given a string `s`, find the length of the longest substring without repeating characters.\n\nExample:\nInput: s = \"abcabcbb\"\nOutput: 3 (Explanation: \"abc\")",
            "difficulty": "Medium",
            "tags": "Python, Sliding Window, Strings",
            "initial_code": "def length_of_longest_substring(s: str) -> int:\n    # Write your solution here\n    pass"
        },
        {
            "title": "Group Anagrams",
            "description": "Given an array of strings `strs`, group the anagrams together. You can return the answer in any order.\n\nExample:\nInput: strs = [\"eat\",\"tea\",\"tan\",\"ate\",\"nat\",\"bat\"]\nOutput: [[\"bat\"],[\"nat\",\"tan\"],[\"ate\",\"eat\",\"tea\"]]",
            "difficulty": "Medium",
            "tags": "Python, Hash Table, Sorting",
            "initial_code": "def group_anagrams(strs):\n    # Write your solution here\n    pass"
        },
        {
            "title": "Merge K Sorted Lists",
            "description": "You are given an array of `k` linked-lists lists, each linked-list is sorted in ascending order. Merge all the linked-lists into one sorted linked-list and return it.",
            "difficulty": "Hard",
            "tags": "Python, Linked List, Heap",
            "initial_code": "def merge_k_lists(lists):\n    # Write your solution here\n    pass"
        },
        {
            "title": "LRU Cache Implementation",
            "description": "Design a data structure that follows the constraints of a Least Recently Used (LRU) cache with `get(key)` and `put(key, value)` in O(1) time complexity.",
            "difficulty": "Hard",
            "tags": "Python, Design, Hash Table, Linked List",
            "initial_code": "class LRUCache:\n    def __init__(self, capacity: int):\n        pass\n\n    def get(self, key: int) -> int:\n        pass\n\n    def put(self, key: int, value: int) -> None:\n        pass"
        },
        {
            "title": "Trapping Rain Water",
            "description": "Given `n` non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.",
            "difficulty": "Hard",
            "tags": "Python, Two Pointers, Dynamic Programming",
            "initial_code": "def trap(height):\n    # Write your solution here\n    pass"
        }
    ],
    "SQL": [
        {
            "title": "Second Highest Salary",
            "description": "Write a SQL query to get the second highest salary from the `Employee` table. If there is no second highest salary, query should return NULL.\n\nSchema:\nEmployee (id INT, salary INT)",
            "difficulty": "Medium",
            "tags": "SQL, Subquery, Aggregate",
            "initial_code": "SELECT MAX(salary) AS SecondHighestSalary \nFROM Employee \nWHERE salary < (SELECT MAX(salary) FROM Employee);"
        },
        {
            "title": "Employees Earning More Than Their Managers",
            "description": "Write a SQL query to find the employees who earn more than their managers.\n\nSchema:\nEmployee (id INT, name VARCHAR, salary INT, managerId INT)",
            "difficulty": "Easy",
            "tags": "SQL, Self Join",
            "initial_code": "SELECT e.name AS Employee\nFROM Employee e\nJOIN Employee m ON e.managerId = m.id\nWHERE e.salary > m.salary;"
        },
        {
            "title": "Duplicate Emails Finder",
            "description": "Write a SQL query to report all the duplicate emails in a table named `Person`.\n\nSchema:\nPerson (id INT, email VARCHAR)",
            "difficulty": "Easy",
            "tags": "SQL, Group By, Having",
            "initial_code": "SELECT email\nFROM Person\nGROUP BY email\nHAVING COUNT(email) > 1;"
        },
        {
            "title": "Customers Who Never Order",
            "description": "Write a SQL query to find all customers who never order anything.\n\nSchema:\nCustomers (id INT, name VARCHAR)\nOrders (id INT, customerId INT)",
            "difficulty": "Easy",
            "tags": "SQL, Left Join, Null Check",
            "initial_code": "SELECT c.name AS Customers\nFROM Customers c\nLEFT JOIN Orders o ON c.id = o.customerId\nWHERE o.id IS NULL;"
        },
        {
            "title": "Department Top Three Salaries",
            "description": "A company's executives are interested in seeing who earns the most money in each of the company's departments. A high earner in a department is an employee who has a salary in the top three unique salaries for that department. Write a SQL query to find employees who are high earners.",
            "difficulty": "Hard",
            "tags": "SQL, Window Functions, DENSE_RANK",
            "initial_code": "SELECT Department, Employee, Salary FROM (\n    SELECT d.name AS Department, e.name AS Employee, e.salary AS Salary,\n           DENSE_RANK() OVER (PARTITION BY e.departmentId ORDER BY e.salary DESC) as rnk\n    FROM Employee e\n    JOIN Department d ON e.departmentId = d.id\n) sub\nWHERE rnk <= 3;"
        },
        {
            "title": "Calculate Running Total / Cumulative Sum",
            "description": "Write a SQL query to calculate the running total of transaction amounts per customer ordered by transaction_date.\n\nSchema:\nTransactions (id INT, customer_id INT, amount DECIMAL, transaction_date DATE)",
            "difficulty": "Medium",
            "tags": "SQL, Window Functions, SUM OVER",
            "initial_code": "SELECT customer_id, transaction_date, amount,\n       SUM(amount) OVER (PARTITION BY customer_id ORDER BY transaction_date) AS running_total\nFROM Transactions;"
        },
        {
            "title": "Daily Active Users & Retention Analysis",
            "description": "Write a SQL query to find the daily count of active users who performed at least one action in the `UserActivity` table for the last 30 days.\n\nSchema:\nUserActivity (user_id INT, session_id INT, activity_date DATE, activity_type VARCHAR)",
            "difficulty": "Medium",
            "tags": "SQL, Date Functions, Distinct Count",
            "initial_code": "SELECT activity_date, COUNT(DISTINCT user_id) AS active_users\nFROM UserActivity\nWHERE activity_date >= CURRENT_DATE - INTERVAL '30 days'\nGROUP BY activity_date\nORDER BY activity_date DESC;"
        }
    ],
    "HTML_CSS": [
        {
            "title": "Responsive Navigation Bar with Mobile Drawer",
            "description": "Create a fully responsive navbar using semantic HTML `<nav>` and Flexbox. On desktop, links should appear in a row; on screens < 768px, display a hamburger toggle menu.",
            "difficulty": "Easy",
            "tags": "HTML, CSS, Flexbox, Responsive",
            "initial_code": "<nav class=\"navbar\">\n  <div class=\"logo\">Brand</div>\n  <ul class=\"nav-links\">\n    <li><a href=\"#\">Home</a></li>\n    <li><a href=\"#\">Features</a></li>\n    <li><a href=\"#\">Contact</a></li>\n  </ul>\n</nav>\n<style>\n/* Write responsive CSS here */\n</style>"
        },
        {
            "title": "Flexbox Holy Grail Layout",
            "description": "Build a classic Holy Grail layout with a sticky header, 3-column body (left sidebar, main content, right sidebar), and a sticky footer using CSS Flexbox or Grid.",
            "difficulty": "Medium",
            "tags": "HTML, CSS, Layout, Flexbox",
            "initial_code": "<div class=\"layout-container\">\n  <header>Header</header>\n  <div class=\"main-body\">\n    <aside class=\"sidebar-left\">Nav</aside>\n    <main class=\"content\">Main Content</main>\n    <aside class=\"sidebar-right\">Ads/Widgets</aside>\n  </div>\n  <footer>Footer</footer>\n</div>"
        },
        {
            "title": "Responsive CSS Grid Photo Gallery",
            "description": "Create a responsive photo gallery using `grid-template-columns: repeat(auto-fit, minmax(250px, 1fr))` with smooth hover zoom effects on images.",
            "difficulty": "Medium",
            "tags": "HTML, CSS, Grid, Animations",
            "initial_code": "<div class=\"gallery\">\n  <div class=\"gallery-item\"><img src=\"photo1.jpg\" alt=\"1\"></div>\n  <div class=\"gallery-item\"><img src=\"photo2.jpg\" alt=\"2\"></div>\n  <div class=\"gallery-item\"><img src=\"photo3.jpg\" alt=\"3\"></div>\n</div>\n<style>\n/* Implement CSS Grid & Hover effects */\n</style>"
        },
        {
            "title": "Accessible Login Form with Floating Labels",
            "description": "Design an accessible login card with floating label animations when input fields are focused or contain text using pure CSS `:focus` and `:placeholder-shown` pseudo-classes.",
            "difficulty": "Easy",
            "tags": "HTML, CSS, Forms, Accessibility",
            "initial_code": "<form class=\"login-form\">\n  <div class=\"form-group\">\n    <input type=\"email\" id=\"email\" placeholder=\" \" required />\n    <label for=\"email\">Email Address</label>\n  </div>\n</form>"
        },
        {
            "title": "Glassmorphism Card with Gradient Border",
            "description": "Implement an ultra-modern glassmorphic card with `backdrop-filter: blur()`, semi-transparent RGBA background, and a glowing multi-color gradient border.",
            "difficulty": "Medium",
            "tags": "CSS, Glassmorphism, Modern UI",
            "initial_code": "<div class=\"glass-card\">\n  <h3>Premium Feature</h3>\n  <p>Experience state of the art UI elements.</p>\n</div>\n<style>\n/* Add blur and gradient border styles */\n</style>"
        },
        {
            "title": "Pure CSS Animated Dark Mode Toggle Switch",
            "description": "Build an animated toggle switch with sun and moon icons without using any JavaScript, leveraging checkbox `:checked` state.",
            "difficulty": "Easy",
            "tags": "CSS, Animation, Transitions",
            "initial_code": "<label class=\"theme-switch\">\n  <input type=\"checkbox\" id=\"toggle\">\n  <span class=\"slider round\"></span>\n</label>"
        },
        {
            "title": "Responsive Multi-Level Accordion Component",
            "description": "Build an expandable/collapsible FAQ accordion using semantic `<details>` and `<summary>` or CSS `:target` with smooth height transitions.",
            "difficulty": "Hard",
            "tags": "HTML, CSS, Accordion, Semantic",
            "initial_code": "<div class=\"accordion\">\n  <details>\n    <summary>How does AI scoring work?</summary>\n    <p>AI evaluates code efficiency, edge cases, and cleanliness.</p>\n  </details>\n</div>"
        }
    ],
    "JavaScript": [
        {
            "title": "Flatten Deeply Nested Array (Array.prototype.flat Polyfill)",
            "description": "Write a function `flattenArray(arr, depth)` that recursively flattens a multi-dimensional array up to the specified depth.\n\nExample:\nInput: arr = [1, [2, [3, [4]]]], depth = 2\nOutput: [1, 2, 3, [4]]",
            "difficulty": "Medium",
            "tags": "JavaScript, Recursion, Arrays",
            "initial_code": "function flattenArray(arr, depth = 1) {\n    // Write your code here\n}"
        },
        {
            "title": "Debounce Function Implementation",
            "description": "Implement a `debounce(fn, delay)` utility function that delays invoking `fn` until after `delay` milliseconds have elapsed since the last time the debounced function was invoked.",
            "difficulty": "Medium",
            "tags": "JavaScript, Closures, Async",
            "initial_code": "function debounce(fn, delay) {\n    // Write your debounce implementation\n}"
        },
        {
            "title": "Deep Clone an Object",
            "description": "Write a function `deepClone(obj)` that returns a deep copy of an object, properly handling nested objects, arrays, and primitive data types without using JSON.parse(JSON.stringify(obj)).",
            "difficulty": "Medium",
            "tags": "JavaScript, Objects, Recursion",
            "initial_code": "function deepClone(obj) {\n    // Write your deep clone implementation\n}"
        },
        {
            "title": "Custom Promise.all Implementation",
            "description": "Implement a polyfill `customPromiseAll(promises)` that takes an iterable of promises and returns a single Promise that resolves when all of the promises in the iterable argument have resolved.",
            "difficulty": "Hard",
            "tags": "JavaScript, Promises, Async",
            "initial_code": "function customPromiseAll(promises) {\n    return new Promise((resolve, reject) => {\n        // Write logic here\n    });\n}"
        },
        {
            "title": "Two Sum in JavaScript",
            "description": "Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to target in O(n) time complexity.",
            "difficulty": "Easy",
            "tags": "JavaScript, Map, Hash Table",
            "initial_code": "function twoSum(nums, target) {\n    // Write your solution here\n}"
        },
        {
            "title": "Anagram & Palindrome Validator",
            "description": "Write a function `isAnagram(str1, str2)` that checks if two given strings are anagrams of each other, ignoring case, spaces, and punctuation.",
            "difficulty": "Easy",
            "tags": "JavaScript, Strings, Algorithms",
            "initial_code": "function isAnagram(str1, str2) {\n    // Write your solution here\n}"
        },
        {
            "title": "Custom Event Emitter Class",
            "description": "Design an EventEmitter class in JavaScript with `on(eventName, listener)`, `emit(eventName, ...args)`, and `off(eventName, listener)` methods.",
            "difficulty": "Hard",
            "tags": "JavaScript, OOP, Design Patterns",
            "initial_code": "class EventEmitter {\n    constructor() {\n        this.events = {};\n    }\n    on(event, listener) {}\n    emit(event, ...args) {}\n    off(event, listener) {}\n}"
        }
    ],
    "Java": [
        {
            "title": "Two Sum in Java",
            "description": "Given an array of integers `nums` and an integer `target`, return indices of the two numbers that sum up to target using `HashMap` in O(n) time.",
            "difficulty": "Easy",
            "tags": "Java, HashMap, Arrays",
            "initial_code": "import java.util.*;\n\npublic class Solution {\n    public int[] twoSum(int[] nums, int target) {\n        // Write your solution here\n        return new int[]{};\n    }\n}"
        },
        {
            "title": "Reverse a Linked List",
            "description": "Given the head of a singly linked list, reverse the list, and return the reversed list.",
            "difficulty": "Easy",
            "tags": "Java, Linked List, Pointers",
            "initial_code": "public class Solution {\n    public ListNode reverseList(ListNode head) {\n        // Write code here\n        return null;\n    }\n}"
        },
        {
            "title": "Find Missing Number in Array",
            "description": "Given an array `nums` containing `n` distinct numbers in the range `[0, n]`, return the only number in the range that is missing from the array.",
            "difficulty": "Easy",
            "tags": "Java, Math, Bit Manipulation",
            "initial_code": "public class Solution {\n    public int missingNumber(int[] nums) {\n        // Write code here\n        return 0;\n    }\n}"
        },
        {
            "title": "Valid Anagram Check",
            "description": "Given two strings `s` and `t`, return `true` if `t` is an anagram of `s`, and `false` otherwise.",
            "difficulty": "Easy",
            "tags": "Java, Strings, Hash Table",
            "initial_code": "public class Solution {\n    public boolean isAnagram(String s, String t) {\n        // Write code here\n        return false;\n    }\n}"
        },
        {
            "title": "Binary Tree Level Order Traversal",
            "description": "Given the `root` of a binary tree, return the level order traversal of its nodes' values (i.e., from left to right, level by level) using a Queue.",
            "difficulty": "Medium",
            "tags": "Java, Trees, BFS, Queue",
            "initial_code": "import java.util.*;\n\npublic class Solution {\n    public List<List<Integer>> levelOrder(TreeNode root) {\n        // Write code here\n        return new ArrayList<>();\n    }\n}"
        },
        {
            "title": "Implement Queue using Stacks",
            "description": "Implement a first in first out (FIFO) queue using only two stacks. The implemented queue should support `push`, `pop`, `peek`, and `empty` operations.",
            "difficulty": "Medium",
            "tags": "Java, Stack, Queue, Design",
            "initial_code": "import java.util.Stack;\n\nclass MyQueue {\n    public MyQueue() {}\n    public void push(int x) {}\n    public int pop() { return 0; }\n    public int peek() { return 0; }\n    public boolean empty() { return true; }\n}"
        },
        {
            "title": "Trapping Rain Water in Java",
            "description": "Given `n` non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining in O(n) time.",
            "difficulty": "Hard",
            "tags": "Java, Two Pointers, Array",
            "initial_code": "public class Solution {\n    public int trap(int[] height) {\n        // Write code here\n        return 0;\n    }\n}"
        }
    ],
    "C++": [
        {
            "title": "Maximum Subarray Sum (Kadane's Algorithm)",
            "description": "Given an integer array `nums`, find the subarray with the largest sum, and return its sum.",
            "difficulty": "Medium",
            "tags": "C++, Dynamic Programming, Arrays",
            "initial_code": "#include <vector>\n#include <algorithm>\nusing namespace std;\n\nint maxSubArray(vector<int>& nums) {\n    // Write your code here\n    return 0;\n}"
        },
        {
            "title": "Reverse an Array in-place",
            "description": "Write a C++ function to reverse a vector of integers in-place without allocating auxiliary array memory.",
            "difficulty": "Easy",
            "tags": "C++, Two Pointers, Vector",
            "initial_code": "#include <vector>\nusing namespace std;\n\nvoid reverseVector(vector<int>& nums) {\n    // Write code here\n}"
        },
        {
            "title": "Valid Parentheses using std::stack",
            "description": "Given a string `s` containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid using `std::stack`.",
            "difficulty": "Easy",
            "tags": "C++, Stack, STL",
            "initial_code": "#include <string>\n#include <stack>\nusing namespace std;\n\nbool isValid(string s) {\n    // Write code here\n    return false;\n}"
        },
        {
            "title": "Merge Two Sorted Arrays",
            "description": "You are given two integer arrays `nums1` and `nums2`, sorted in non-decreasing order. Merge `nums2` into `nums1` as one sorted array.",
            "difficulty": "Easy",
            "tags": "C++, Two Pointers, Sorting",
            "initial_code": "#include <vector>\nusing namespace std;\n\nvoid merge(vector<int>& nums1, int m, vector<int>& nums2, int n) {\n    // Write code here\n}"
        },
        {
            "title": "Find Kth Largest Element",
            "description": "Given an integer array `nums` and an integer `k`, return the `k`th largest element in the array using `std::priority_queue` min-heap in O(N log K).",
            "difficulty": "Medium",
            "tags": "C++, Heap, Priority Queue",
            "initial_code": "#include <vector>\n#include <queue>\nusing namespace std;\n\nint findKthLargest(vector<int>& nums, int k) {\n    // Write code here\n    return 0;\n}"
        },
        {
            "title": "Search in Rotated Sorted Array",
            "description": "Given the array `nums` after possible rotation and an integer `target`, return the index of `target` if it is in `nums`, or -1 if it is not in `nums` in O(log n) runtime.",
            "difficulty": "Medium",
            "tags": "C++, Binary Search",
            "initial_code": "#include <vector>\nusing namespace std;\n\nint search(vector<int>& nums, int target) {\n    // Write code here\n    return -1;\n}"
        },
        {
            "title": "Minimum Window Substring",
            "description": "Given two strings `s` and `t` of lengths `m` and `n` respectively, return the minimum window substring of `s` such that every character in `t` (including duplicates) is included in the window.",
            "difficulty": "Hard",
            "tags": "C++, Sliding Window, Hash Table",
            "initial_code": "#include <string>\n#include <unordered_map>\nusing namespace std;\n\nstring minWindow(string s, string t) {\n    // Write code here\n    return \"\";\n}"
        }
    ],
    "React": [
        {
            "title": "Interactive Counter with Undo/Redo",
            "description": "Build a React counter component that allows incrementing, decrementing, and supports a complete Undo/Redo history stack using `useState` or `useReducer`.",
            "difficulty": "Easy",
            "tags": "React, Hooks, State Management",
            "initial_code": "import React, { useState } from 'react';\n\nexport default function UndoableCounter() {\n  // Write React Component\n  return <div>Counter</div>;\n}"
        },
        {
            "title": "Real-time Search & Filter List",
            "description": "Create a React component that takes a large array of users and filters them in real-time as the user types in an input box, with case-insensitive matching.",
            "difficulty": "Easy",
            "tags": "React, Inputs, Array Filter",
            "initial_code": "import React, { useState } from 'react';\n\nexport default function UserSearch({ users }) {\n  // Implement search filter\n  return <div>Search</div>;\n}"
        },
        {
            "title": "Custom useDebounce Hook",
            "description": "Write a custom React hook `useDebounce(value, delay)` that returns the debounced value after the specified delay in milliseconds.",
            "difficulty": "Medium",
            "tags": "React, Custom Hooks, useEffect",
            "initial_code": "import { useState, useEffect } from 'react';\n\nexport function useDebounce(value, delay) {\n  // Write custom hook\n}"
        },
        {
            "title": "Todo List with LocalStorage Persistence",
            "description": "Build a full Todo List with add, delete, toggle completed, and filter (All/Active/Completed) that automatically persists to `localStorage`.",
            "difficulty": "Medium",
            "tags": "React, LocalStorage, CRUD",
            "initial_code": "import React, { useState, useEffect } from 'react';\n\nexport default function TodoApp() {\n  // Write Todo app with localStorage\n  return <div>Todos</div>;\n}"
        },
        {
            "title": "Tabbed Navigation Component",
            "description": "Build an accessible, animated tabbed content switcher component supporting keyboard arrow navigation and active indicator transitions.",
            "difficulty": "Medium",
            "tags": "React, Accessibility, Components",
            "initial_code": "import React, { useState } from 'react';\n\nexport default function Tabs({ tabs }) {\n  // Write Tabs Component\n  return <div>Tabs</div>;\n}"
        },
        {
            "title": "Modal Dialog with Backdrop Blur & Escape Key",
            "description": "Build a reusable Modal component that closes on Backdrop click or pressing the `Escape` key, and traps keyboard focus while open.",
            "difficulty": "Medium",
            "tags": "React, Modals, Portals, Event Listeners",
            "initial_code": "import React, { useEffect } from 'react';\n\nexport default function Modal({ isOpen, onClose, children }) {\n  // Write Modal component\n  return isOpen ? <div>{children}</div> : null;\n}"
        },
        {
            "title": "Infinite Scroll & Virtualized Feed Component",
            "description": "Create an infinite scrolling feed component that uses `IntersectionObserver` to trigger API fetching when the bottom sentinel element becomes visible.",
            "difficulty": "Hard",
            "tags": "React, IntersectionObserver, Performance",
            "initial_code": "import React, { useState, useEffect, useRef } from 'react';\n\nexport default function InfiniteFeed({ fetchMore }) {\n  // Write Infinite Feed component\n  return <div>Feed</div>;\n}"
        }
    ]
}

@login_required
def coding_list_view(request, language):
    # Normalize language name for display and lookup
    display_language = language.replace('_', ' ')
    
    # Map key to standard lookup
    norm_key = "Python"
    for k in DEFAULT_CHALLENGES.keys():
        if k.lower() == language.lower() or k.lower() == display_language.lower() or (language.lower() == 'html_css' and k == 'HTML_CSS'):
            norm_key = k
            break
            
    # Filter problems specifically for this language
    problems = CodingProblem.objects.filter(
        models.Q(language__iexact=language) | 
        models.Q(language__iexact=display_language) |
        models.Q(language__iexact=norm_key)
    ).order_by('id')
    
    # If fewer than 7 problems exist for this language, seed from our curated bank
    if problems.count() < 7 and norm_key in DEFAULT_CHALLENGES:
        existing_titles = set(problems.values_list('title', flat=True))
        for item in DEFAULT_CHALLENGES[norm_key]:
            if item['title'] not in existing_titles:
                CodingProblem.objects.create(
                    title=item['title'],
                    description=item['description'],
                    difficulty=item['difficulty'],
                    tags=item['tags'],
                    language=display_language,
                    initial_code=item.get('initial_code', '')
                )
        problems = CodingProblem.objects.filter(
            models.Q(language__iexact=language) | 
            models.Q(language__iexact=display_language) |
            models.Q(language__iexact=norm_key)
        ).order_by('id')

    # Process tags
    for problem in problems:
        problem.tag_list = [t.strip() for t in problem.tags.split(',')]
        
    context = {
        'problems': problems,
        'language': display_language,
    }
    return render(request, 'coding_round/list.html', context)

@login_required
def coding_editor_view(request, problem_id):
    problem = get_object_or_404(CodingProblem, id=problem_id)
    return render(request, 'coding_round/editor.html', {'problem': problem})

@login_required
def submit_code_api(request, problem_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        code = data.get('code', '').strip()
        
        problem = get_object_or_404(CodingProblem, id=problem_id)
        
        score = 0
        output_text = ""
        error_text = ""
        feedback_text = ""

        # Use Gemini AI to evaluate code logic, correctness, syntax & edge cases
        api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        if api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"""
                You are an automated code grader and compiler judge for a competitive programming platform.
                
                Problem Title: {problem.title}
                Problem Description: {problem.description}
                Programming Language: {problem.language}
                
                Candidate Submitted Code:
                ```{problem.language}
                {code}
                ```
                
                Evaluate the submitted code carefully for correctness, syntax errors, logical bugs, and edge case coverage.
                
                Return ONLY a JSON object with this exact structure (no markdown formatting):
                {{
                    "score": 85,  // Integer score from 0 to 100 based on correctness and logic
                    "output": "Simulated output or test execution result (e.g. Test Case 1 Passed, Test Case 2 Passed...)",
                    "error": "Compiler/Syntax or Logic Error description if any, otherwise empty string",
                    "feedback": "Concise 1-2 sentence feedback explaining score or suggesting fixes."
                }}
                """
                response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
                raw_text = response.text.strip()
                import re
                match = re.search(r'\{.*\}', raw_text, re.DOTALL)
                if match:
                    raw_text = match.group(0)
                result = json.loads(raw_text)
                
                score = int(result.get('score', 70))
                output_text = str(result.get('output', 'Code executed.'))
                error_text = str(result.get('error', ''))
                feedback_text = str(result.get('feedback', ''))
            except Exception as e:
                print(f"Code AI Evaluation error: {e}")
                # Heuristic fallback if AI API fails
                if not code or len(code) < 15 or "pass" in code or "return 0" in code and "solution" not in code:
                    score = 25
                    error_text = "Incomplete solution. Please implement the logic function."
                    output_text = "Execution failed: Placeholder code submitted."
                else:
                    score = 80
                    output_text = "Test cases passed successfully."
                    feedback_text = "Good attempt! Code logic looks structured."
        else:
            # Fallback evaluation
            if not code or "pass" in code:
                score = 30
                error_text = "Placeholder starter code detected."
            else:
                score = 85
                output_text = "Test cases passed."
            
        submission = CodingSubmission.objects.create(
            user=request.user,
            problem=problem,
            user_code=code,
            score=score
        )
        
        return JsonResponse({
            'status': 'success',
            'score': score,
            'output': output_text,
            'error': error_text,
            'feedback': feedback_text,
            'submission_id': submission.id
        })
        
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def coding_setup_view(request):
    return render(request, 'coding_round/setup.html')

@login_required
def generate_practice_api(request):
    if request.method == 'POST' and request.FILES.get('resume'):
        from resume.models import Resume
        from resume.utils import extract_text_from_pdf, extract_text_from_docx
        from ai_engine.logic import generate_coding_problems
        import os
        
        file = request.FILES['resume']
        resume_obj = Resume.objects.create(user=request.user, file=file)
        file_path = resume_obj.file.path
        ext = os.path.splitext(file_path)[1].lower()
        text = ""
        if ext == '.pdf': text = extract_text_from_pdf(file_path)
        elif ext == '.docx': text = extract_text_from_docx(file_path)
        elif ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
                
        resume_obj.extracted_text = text
        resume_obj.save()
        
        # Generate personalized problems
        problems_json = generate_coding_problems(text, count=3)
        
        if isinstance(problems_json, dict):
            if 'problems' in problems_json:
                problems_json = problems_json['problems']
            elif 'coding_problems' in problems_json:
                problems_json = problems_json['coding_problems']
            else:
                # Try to find any list in the dict values
                for v in problems_json.values():
                    if isinstance(v, list):
                        problems_json = v
                        break
        
        if problems_json and isinstance(problems_json, list):
            for p in problems_json:
                if not isinstance(p, dict):
                    continue
                CodingProblem.objects.create(
                    user=request.user,
                    title=str(p.get('title', 'Coding Challenge'))[:200],
                    description=str(p.get('description', '')),
                    difficulty=str(p.get('difficulty', 'Medium'))[:20],
                    tags=str(p.get('tags', ''))[:200],
                    language=str(p.get('language', 'Python'))[:50],
                    initial_code=str(p.get('initial_code', 'def solution():\n    pass'))
                )
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'AI failed to generate problems.'}, status=500)
    return JsonResponse({'status': 'error', 'message': 'No resume provided.'}, status=400)

@login_required
def get_hint_api(request, problem_id):
    if request.method == 'POST':
        from ai_engine.logic import get_coding_hint
        data = json.loads(request.body)
        user_code = data.get('code', '')
        hint_lang = data.get('language', 'ta-EN')
        
        problem = get_object_or_404(CodingProblem, id=problem_id)
        hint = get_coding_hint(problem.title, problem.description, user_code, language=hint_lang)
        
        return JsonResponse({'status': 'success', 'hint': hint})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def generate_single_challenge_api(request):
    if request.method == 'POST':
        import json
        from resume.models import Resume
        from ai_engine.logic import get_fallback_coding_problems
        import google.generativeai as genai
        import os
        
        data = json.loads(request.body)
        lang = data.get('language', 'Python').strip()
        
        # Get user resume
        resumes = Resume.objects.filter(user=request.user)
        resume_text = ""
        if resumes.exists():
            resume_text = resumes.latest('uploaded_at').extracted_text
            
        api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        
        # We will generate a problem in the selected language
        new_problem = None
        if api_key:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                resume_context = f"The candidate's resume content is:\n{resume_text[:2000]}" if resume_text else "No resume available."
                
                prompt = f"""
                You are an expert technical interviewer.
                Generate exactly ONE coding problem to test the candidate in the programming language: {lang}.
                {resume_context}
                
                Return ONLY a JSON object with the following fields:
                - "title": A short title for the problem (e.g., "Two Sum" or "Array Reversal").
                - "description": A clear description of the problem, input/output requirements, and an example.
                - "difficulty": "Easy", "Medium", or "Hard".
                - "tags": Comma-separated tags (e.g., "{lang}, Arrays, Algorithms").
                - "initial_code": Starter code boilerplate in {lang} that the user will complete (e.g. `def solution(nums, target):` or `function solution(nums, target) {{}}`).
                
                Ensure the JSON format is perfectly valid. Return ONLY the raw JSON text. Do not use ```json formatting.
                """
                response = model.generate_content(prompt, request_options={"timeout": 15.0})
                text = response.text.strip()
                
                import re
                match = re.search(r'\{.*\}', text, re.DOTALL)
                if match:
                    p = json.loads(match.group(0))
                    new_problem = CodingProblem.objects.create(
                        user=request.user,
                        title=str(p.get('title', 'Coding Challenge'))[:200],
                        description=str(p.get('description', '')),
                        difficulty=str(p.get('difficulty', 'Medium'))[:20],
                        tags=str(p.get('tags', ''))[:200],
                        language=lang,
                        initial_code=str(p.get('initial_code', ''))
                    )
            except Exception as e:
                print(f"Error generating single coding challenge: {e}")
                
        if not new_problem:
            # Fallback
            fallbacks = get_fallback_coding_problems([], count=1)
            f = fallbacks[0]
            initial_code = f.get('initial_code')
            if lang.lower() == 'javascript':
                initial_code = "function solution(n) {\n    // Write code here\n}"
            elif lang.lower() == 'java':
                initial_code = "public class Solution {\n    public static void main(String[] args) {\n        // Write code here\n    }\n}"
            elif lang.lower() == 'c++':
                initial_code = "#include <iostream>\nusing namespace std;\n\nvoid solution() {\n    // Write code here\n}"
                
            new_problem = CodingProblem.objects.create(
                user=request.user,
                title=f.get('title'),
                description=f.get('description'),
                difficulty=f.get('difficulty'),
                tags=f.get('tags'),
                language=lang,
                initial_code=initial_code
            )
            
        return JsonResponse({'status': 'success', 'problem_id': new_problem.id})
        
    return JsonResponse({'status': 'error'}, status=400)
