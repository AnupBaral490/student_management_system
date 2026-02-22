# GPA Calculation Explanation

## Current System

The system now uses a **Weighted GPA** calculation that gives more importance to exams with higher total marks.

## Example Calculation

Using your actual data:

### Exam Results:
1. Mid-term Exam - Sociology: 55/100 = 55% → Grade: C+ → Grade Point: 2.3
2. Mid-term Exam - Data Warehousing: 62/100 = 62% → Grade: B → Grade Point: 3.0
3. Mid-term Exam - E-commerce: 65/100 = 65% → Grade: B → Grade Point: 3.0
4. Mid-term Exam - Operation Management: 62/100 = 62% → Grade: B → Grade Point: 3.0
5. Mid-term Exam - Strategic Management: 77/100 = 77% → Grade: B+ → Grade Point: 3.3
6. JKL - Sociology: 22/100 = 22% → Grade: F → Grade Point: 0.0
7. ABC - Sociology: 33/40 = 82.5% → Grade: A → Grade Point: 3.7

### Grade Point Scale:
- A+ (90-100%): 4.0
- A (80-89%): 3.7
- B+ (70-79%): 3.3
- B (60-69%): 3.0
- C+ (50-59%): 2.3
- C (40-49%): 2.0
- D (30-39%): 1.0
- F (0-29%): 0.0

## Two Calculation Methods

### Method 1: Simple Average GPA (Previous Method)
Each exam counts equally, regardless of total marks.

**Formula:** GPA = Sum of all grade points / Number of exams

**Calculation:**
```
Total Grade Points = 2.3 + 3.0 + 3.0 + 3.0 + 3.3 + 0.0 + 3.7 = 18.3
Number of Exams = 7
GPA = 18.3 / 7 = 2.61
```

**Result: 2.61 GPA**

### Method 2: Weighted Average GPA (New Method)
Exams with more marks have more weight in the calculation.

**Formula:** GPA = Sum of (Grade Point × Total Marks) / Sum of Total Marks

**Calculation:**
```
Weighted Points:
- Sociology: 2.3 × 100 = 230
- Data Warehousing: 3.0 × 100 = 300
- E-commerce: 3.0 × 100 = 300
- Operation Management: 3.0 × 100 = 300
- Strategic Management: 3.3 × 100 = 330
- JKL: 0.0 × 100 = 0
- ABC: 3.7 × 40 = 148

Total Weighted Points = 230 + 300 + 300 + 300 + 330 + 0 + 148 = 1,608
Total Credits (Marks) = 100 + 100 + 100 + 100 + 100 + 100 + 40 = 640

GPA = 1,608 / 640 = 2.51
```

**Result: 2.51 GPA**

## Which Method is Better?

### Simple Average (2.61)
**Pros:**
- Easy to understand
- Each exam counts equally
- Fair when all exams are equally important

**Cons:**
- A 40-mark exam has the same weight as a 100-mark exam
- Doesn't reflect the actual workload/importance

### Weighted Average (2.51)
**Pros:**
- More accurate representation of overall performance
- Reflects the importance/weight of each exam
- Standard in most educational institutions
- A 100-mark exam has more impact than a 40-mark exam

**Cons:**
- Slightly more complex to understand

## Current Implementation

The system now uses the **Weighted Average** method by default, as it's more academically accurate and fair.

If you want to switch back to the Simple Average method, you can edit the file:
`examination/views.py` (around line 95-105)

Comment out the weighted calculation and uncomment the simple average lines:

```python
# Weighted GPA (current - comment these lines)
# weighted_points_sum = 0
# total_credits = 0
# for result in results:
#     grade_point = grade_points.get(result.grade, 0.0)
#     credit = result.examination.total_marks
#     weighted_points_sum += grade_point * credit
#     total_credits += credit
# gpa = (weighted_points_sum / total_credits) if total_credits > 0 else 0.0

# Simple average GPA (uncomment these lines)
total_points = sum(grade_points.get(result.grade, 0.0) for result in results)
gpa = total_points / total_exams if total_exams > 0 else 0.0
```

## Overall Grade Calculation

The overall grade is based on the average percentage across all exams:

**Formula:** Average % = Total Marks Obtained / Total Marks Possible × 100

**Your Calculation:**
```
Total Obtained = 55 + 62 + 65 + 62 + 77 + 22 + 33 = 376
Total Possible = 100 + 100 + 100 + 100 + 100 + 100 + 40 = 640
Average % = 376 / 640 × 100 = 58.75% ≈ 58.8%

Grade: C+ (50-59%)
```

This matches your displayed result of 58.8% and C+ grade.
