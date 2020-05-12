# New hire onboarding to Endpoint Team


### Scheduling meet and greets for the first few weeks
- Groups / Individuals
	- QA 
	- Sensor Team 
	- Endpoint Management
	- Endpoint Response
	- Docs
	- SIEM - Tudor
	- Chris Owens
	- Sean C
	- Tony Meehan
	- Having hour long session with former Endgame Product to go over the Endgame Platform


### First week & resources
- Compliance training
- Getting setup with Kibana dev / understanding CI / committing to Kibana
- Deploying a Endpoint
- Where we keep issues/our data schema for Endpoint [here](https://github.com/elastic/endpoint-app-team) which is in [Elastic Common Schema - ECS](https://www.elastic.co/guide/en/ecs/current/index.html)
    

- If you sign up with your Elastic email to https://cloud.elastic.co/  you’ll be able  to spin up cloud instances of the Elastic stack for free


- [Security team org structure](https://docs.google.com/spreadsheets/d/1fXe9ZufaukHk9ev8m7j0zpG6gwI0IZhxE7QDIBTcIsQ/edit?usp=drive_web&ouid=115517477838301070374)


- [Past weekly updates for security](https://docs.google.com/document/u/1/d/15Mp50TF_xillXw8Qh3h3p382R8giOe6afLXnxadH9FA/edit?usp=drive_web&ouid=115517477838301070374)


- https://wiki.elastic.co/display/AD/New+Hire+Resources

- If you want do any Elasticsearch training classes for free https://wiki.elastic.co/pages/viewpage.action?spaceKey=Edu&title=Employee+requests+for+Elastic+Training+Courses

##### Endgame phases and references
- [Endgame Sensor Management Platform (SMP) knowledge base](https://wiki.elastic.co/pages/viewpage.action?spaceKey=CC&title=SMP+Knowledge+Base+-+Endpoint+Security+Support)

##### Reference terms
- Phase 0: Legacy Endgame program called SMP
- Phase 1: Iterations on Kibana/Elasticsearch Security App adding features during Elastic Stack release to get parity with Endgame (SMP/Phase 0) product
- Phase 2: Deprecation of Phase 0 product line when Phase 1 product is mature enough.






## Notes from previous new Hires

- It’s safe to accept all meeting invites :) 
- There will be lots of acronyms: https://wiki.elastic.co/display/MAR/List+of+acronyms+and+initialisms
- Ask for any initial one on one’s to be recorded if you would like to go back to reference them later on
- General New Hire Wiki: https://wiki.elastic.co/pages/viewpage.action?spaceKey=AD&title=New+Hire+Resources
- Engineering Wiki: https://wiki.elastic.co/display/EN



### Getting Technical: 



##### Getting set up:

Endpoint App Team: https://github.com/elastic/endpoint-app-team

Install ts-node globally: `npm install -g ts-node`

When you get ElasticSearch and Kibana running:

Login details are => username: `elastic` password: `changeme`

Recommend opening IDE in the x-pack directory: https://github.com/elastic/kibana/tree/master/x-pack

Run tests from the x-pack directory
`node scripts/jest [pathToTest]`


Contributing to Kibana and your first PR! https://github.com/elastic/kibana/blob/master/CONTRIBUTING.md


##### Backporting
Make sure to confirm any tags and any links that should be made in your PR
Backported to Elastic

Script: https://github.com/elastic/kibana/blob/master/scripts/backport.js

Config: https://github.com/elastic/kibana/blob/master/.backportrc.json


### Contributing to Endpoint:
- Endpoint issue tracking board: https://github.com/elastic/endpoint-app-team/projects/7
- Endpoint application is located here: https://github.com/elastic/kibana/tree/master/x-pack/plugins/endpoint
    - General folder structure
        - Common: shared across entire app
        - Public: front end code
        - Server: back end code
- Browser support: https://www.elastic.co/support/matrix#matrix_browsers
- Issues list can be located here: https://github.com/elastic/endpoint-app-team/issues
- Pull Requests: https://github.com/elastic/kibana/pulls?q=is%3Aopen+is%3Apr+label%3AFeature%3AEndpoint




### Generally Good Links/References to Have

EUI (Elastic Component Library) https://elastic.github.io/eui/#/

Elastic Training (Employees get it for free!): https://training.elastic.co/
	Demo’s: (More for sales, but gives you an idea of how the product is being marketed to help your understanding)
		Dev:	https://eden.elastic.dev/
                Prod: https://eden.elastic.co/
                
