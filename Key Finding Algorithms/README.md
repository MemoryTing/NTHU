## MIR（Music Information Retrieval）
### Goal
Find the tonic note and major/minor mode of given music, calculate the accuracy. Compare the difference between different datasets.
In Q1.py, we're finding the only key and the mode of one music. In Q5.py, we're detecting local keys of a music piece, and output the key of the piece every second.
### Details of Q1.py
1. Find the tonic note.
    Compute the chromagram of audio data, find the maximal value in the chroma vector and considering the note name corresponding to the maximal value as the tonic pitch.
2. Find major/minor mode.
    Rotate the vector that the tonic note would be the first note of the vector. Then use function pearsonr to find the mode.
    ```
    # The mode of major and minor by music theory.
    MODE = {"major":[1,0,1,0,1,1,0,1,0,1,0,1],
            "minor":[1,0,1,1,0,1,0,1,1,0,1,0]}
    ```
3. Report the accuracy.
    There are two ways to calculate accuracy：
    * the percentage of numbers of correct detection
    * Some error detection results are closer to the ground truth label.
        Therefore, use the scoring rule as bellow
        
        | Relation        | Points |
        | --------------- | ------ |
        | Same            | 1      |
        | 'Perfect fifth' | 0.5    |
        | 'Relative'      | 0.3    |
        | 'Parallel'      | 0.2    |
        
        Calculate new accuracy by the scoring rule.

Instead of using binary templates, assign values to templates according to human perceptual experiments. Repeat the steps above by using new templates.
```
KS   = {"major":[6.35,2.23,3.48,2.33,4.38,4.09,2.52,5.19,2.39,3.66,2.29,2.88],
        "minor":[6.33,2.68,3.52,5.38,2.60,3.53,2.54,4.75,3.98,2.69,3.34,3.17]}
```
### Details of Q5.py
Get the chromagram of the second we want to detect, and detect with 15 seconds before and after. 
Repeat the steps in Q1.py to find the local key.