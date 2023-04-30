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

There are 4 parts in the file

- logsources : all the logsource found in the rules
- logsource questions : boolean question to take the list of logsource
- type questions : boolean question to select a list of logsource questions
- genral questions : boolean question to select a list of type questions

# Todo List

- [ ] check duplicate uuid (with yaml should not be possible)
- [X] check if logsource no more in the sigma rule (only on update)
- [X] add question to select a set of logsource question
- [X] check if logsource question use a invalid uuid logsource
- [X] check if type question use a invalid uuid logsource question
- [X] check if type question use a invalid uuid type question
- [ ] correcting spelling errors 
- [ ] Add cli sigma path option
- [ ] Add a cli quiz
- [ ] Add a output of the quiz

Add an editor , but it is a big works to do...

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
- `uuid_ref` is the list of uuid that you need to use if you answer yes  


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
        uuid_ref:
            - 2a503beb-86f2-4042-8c45-ce03a9973dd4
```

### Auditd

the logsource is `product: linux / service: auditd` and the simple question is `Do you have auditd enable with rules`

```yaml
    b4c9b09d-a5d1-4067-a769-d612dbf756fb:
        information: linux_none_auditd
        ask: Do you have auditd enable with rules
        uuid_ref:
            - 574175b5-fe78-4d52-ad54-926968a8a530
```

## Example for type question
### Windows Sysmon

With a simple question you can select (or avoid) all questions concerning the sysmon logsource for windows
```yaml
    716d9db2-c3bb-4680-ad84-6d52ed2520d6:
        information: select all the Windows Sysmon question
        ask: Do do have sysmon for Windows
        uuid_ref:
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

## Example for General question
### Linux

With a simple question you can select (or avoid) all questions concerning linux (auditd,sysmon, sudo,...)
```yaml
    847c49ae-dc9b-463b-8440-d9eff20abcb4:
        information: The linux folder
        ask: Do you need Linux rules
        uuid_ref:
            - 1c586617-ccef-4274-ab26-a9e707f552eb
            - 714adc3e-cbdc-4907-a3ee-832357ba2e9e
            - 92e67a63-b06e-4a62-98a7-b2d7f8891971
            - c600eb8f-3063-4078-ae8d-e6e6b2438afe
            - aa15bef2-cae3-4a69-8e8e-a836b7bb73e3
            - cc79ea62-140d-4acc-8adc-311995446e85
            - c76bcba4-69ec-406b-bf6b-139cfdceddd3
            - 1bb4e56c-735e-43c7-94e1-6f96537e9ef3
            - 7ca7d81e-b301-4674-b86d-756fe73aaedd
            - 4b0a0a28-4aa1-4353-a977-4f7675df93ae
            - a020a537-60eb-4ced-9318-c49eb28bc290
            - 67f33595-a279-4ed6-9f09-bbbf6eafd4ed
            - 98b6d220-2fdf-4a4c-866c-8956d8eb071f
```
### Zeek

With a simple question you can select (or avoid) all questions concerning Zeek
```yaml
    2baa5340-6676-46e0-8552-716c6164bdd3:
        information: zeek
        ask: Do you need Zeek rules
        uuid_ref:
            - 275c68e1-eefc-4bf0-aae8-646b8776a686
            - fdf678ff-ea70-46f4-8b01-83028d964a38
            - 1718a67a-0f9c-4ab3-9af8-2db8c5d83bb1
            - c838de8c-1452-451c-a607-d9dd436c63b7
            - 415493fa-bccf-4ece-a736-c06d10ee87f2
            - ecf500be-45f9-4d25-b4d9-874aa1d763b7
            - 4b351da2-fd2a-4cec-8a78-525e15594b42
```
