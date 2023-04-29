# sigma_logsource_helper
Small questions to help select the right logsource for effective detection

# Summary

These are questions for selecting the right logsource according to the available information sources.

There is no engine 
And it's a POC, an idea 

# logsource Yaml 

There are 2 parts in the file

- logsources : all the logsource found in the rules
- questions : a boolean question to take the list of logsource

`fhash` for "frack Hash" , is a way to check logsource with a simple string.
It is not pretty but it's works

# Missing

Add a file or a part to select only the correct questions to ask.

# Details

the logsource are from [Sigma](https://github.com/SigmaHQ/sigma-specification/blob/main/Sigma_specification.md#log-source)

```yaml
    4a25e208-4cc7-4c7e-8782-37418172e38b:
        product: jvm
        category: application
        service: none
```

in the question section:
- `fhash` is not use. Should be change to description or context...  
- `ask` is the text of the question, I do not think the `?` is usefull here  
- `logsource` is the list of logsource uuid that you need to use if you answer yes  


## Example
### Powershell
Some reference: 
 - https://learn.microsoft.com/en-us/powershell/scripting/windows-powershell/wmf/whats-new/script-logging?view=powershell-7.3
 - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_logging?view=powershell-5.1
  
the logsource is `product: windows / category: ps_script` and the simple question is `Do you have enable Script Block Logging`

```
    06deb6dd-6b00-4500-bf35-c6d300f51104:
        fhash: windows_ps_script_none
        ask: Do you have enable Script Block Logging
        logsource:
            - 2a503beb-86f2-4042-8c45-ce03a9973dd4
```

### Auditd

the logsource is `product: linux / service: auditd` and the simple question is `Do you have auditd enable with rules`

```
    b4c9b09d-a5d1-4067-a769-d612dbf756fb:
        fhash: linux_none_auditd
        ask: Do you have auditd enable with rules
        logsource:
            - 574175b5-fe78-4d52-ad54-926968a8a530
```
