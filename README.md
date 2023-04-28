# sigma_logsource_helper
Small questions to help select the right logsource for effective detection

# Summary

These are questions for selecting the right logsource according to the available information sources.

There is no engine 
And it's a POC, an idea 

# Yaml 

Create the list of question
```yaml
    q_windows:
        type: question_select
        question: // text of the question
        value_type: multi or simple selection
        value:
            - // text1
            - // text2
        link_type: question or file
        link:
            - list of question for test1
            - list of question for test2
```

Create the list of logsource
```yaml
    q_symon_w1:
        type: logsource_select
        question: // text of the question
        value:
            - Yes
            - No
        link_type: logsource
        link:
            - list of logsource for Yes
```

# Csv

WIP 