# sigma_logsource_helper
Small questions to help select the right logsource for effective detection

# Summary

These are questions for selecting the right logsource according to the available information sources.

There is no engine 
And it's a POC, an idea 


# Python script

It is a simple script to genrerate the logsouce.yml  
It is more a Proof Of Concept than a valid tools

`fhash` for "frack Hash" , is a way to check logsource with a simple string.  
It is not pretty but it's works


# logsource Yaml 

There are 3 parts in the file

- logsources : all the logsource found in the rules
- logsource questions : boolean question to take the list of logsource
- type questions : boolean question to select a list of logsource questions

# Todo List

- [ ] check duplicate uuid
- [ ] check if logsource is deleted ?
- [ ] check if logsource question use a invalide uuid logsource
- [X] add question to select a set of logsource question
- [ ] check if type question use a invalide uuid logsource question
- [ ] correcting spelling errors 


# Details

the logsource are from [Sigma](https://github.com/SigmaHQ/sigma-specification/blob/main/Sigma_specification.md#log-source)

```yaml
    4a25e208-4cc7-4c7e-8782-37418172e38b:
        product: jvm
        category: application
        service: none
```

in the question section:
- `information` give some information.  
- `ask` is the text of the question, I do not think the `?` is usefull here  
- `logsource` is the list of logsource uuid that you need to use if you answer yes  


## Example for boolean question
### Powershell
Some reference: 
 - https://learn.microsoft.com/en-us/powershell/scripting/windows-powershell/wmf/whats-new/script-logging?view=powershell-7.3
 - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_logging?view=powershell-5.1
  
the logsource is `product: windows / category: ps_script` and the simple question is `Do you have enable Script Block Logging`

```yaml
    06deb6dd-6b00-4500-bf35-c6d300f51104:
        information: windows_ps_script_none
        ask: Do you have enable Script Block Logging
        logsource:
            - 2a503beb-86f2-4042-8c45-ce03a9973dd4
```

### Auditd

the logsource is `product: linux / service: auditd` and the simple question is `Do you have auditd enable with rules`

```yaml
    b4c9b09d-a5d1-4067-a769-d612dbf756fb:
        information: linux_none_auditd
        ask: Do you have auditd enable with rules
        logsource:
            - 574175b5-fe78-4d52-ad54-926968a8a530
```

## Example for type question
### Windows Sysmon
With a simple question you can select (or avoid) all questions concerning the sysmon logsource for windows
```yaml
    716d9db2-c3bb-4680-ad84-6d52ed2520d6:
        information: select all the Windows Sysmon question
        ask: Do do have sysmon for Windows
        question:
            - f92289a0-f979-4ab1-8e5b-ef28af929717
            - d7a550a2-ae07-4b09-b36d-dd23914bd878
            - b6c9289f-3cca-4b09-9d55-fb5c6e722ae7
            - c535be75-cfe5-49fd-b42a-9d7033d8f5fc
            - a1a0f2bd-3ac5-4968-8d0e-be9ec823cd44
            - 021eb6a5-da13-4bff-9666-4c4d69785048
            - fa880187-bf82-4a84-bfc7-7045b3933edd
            - f741e3bb-2d53-4f4a-9c72-3050ad815aa3
            - 0cfba4a8-fa88-4feb-8780-002f2e7cdd07
            - 59729905-b504-49cd-8b5b-5bbc2cb1c655
            - 973d3c83-4ad5-4e2c-9ad9-b364a682a81f
            - 0c5e0766-837b-4a13-848f-b5580300c8a0
            - 30a48069-cc06-4171-a118-acb728cf936a
            - eaf69c4f-727a-4b57-a191-fc8dfcb17fb3
            - cf89dba9-fde2-4ace-87b7-c008a68608dc
            - 6d46a837-2e72-41d1-8363-148d8593503a
            - 190ffbf7-b814-455c-a34f-6c12271c2652
            - 1bacab0d-346b-4740-8179-ebd4679eb345
            - 555c9042-b53a-41c7-83fd-30f970f99f2b
            - fe1c7913-3aa8-4ad7-979a-f1949bd2502a
            - 28e6baa8-da8b-4806-813c-c80a7d69a889
            - f5f0efd4-54a6-40c6-a1e6-108f477c4fdb
```
