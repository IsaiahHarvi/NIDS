# Contributing Guidelines

## Testing
- `docker compose up --build`: bring up and attach to the compose services
- `docker compose down`: stop all of the running services
- `docker system prune --volumes -a`: remove all stopped containers and volmes
- `docker volume rm mongo-data`: clear the persistent data stored in mongoDb
- `bun i && bun dev`: when ran under src/app/server + src/app/client you can run the GUI in development mode


## Opening Issues

- **Clear Description:** When opening an issue, the issue title should address the added feature, fix, or enhancement. If further detail is necessary, elaborate in the description to justify its necessity. Details in implementation should be described under the PR
- **Iteration and Weight:** Assign the issue to an appropriate iteration and give it an estimated weight, where each weight of 1 is equal to 4 hours of work.
- **Labels:** Apply relevant labels to categorize the issue correctly. Limit the number of tags to 3 excluding a priority. As an example, most PRs will have some Docker or gRPC element to them, but they shouldnt be labeled as such unless that is their only contribution.  

## PR Titles and Issue Linking

- **PR Title:** PR titles should match exactly the name of its closing issue. In the case of a PR closing multiple issues, the name should capture its significant changes but will be upto the author.
- **Issue Linking:** Every PR must be linked to at least one issue. Please use the GitHub keywords (e.g., "Closes #issue_number") in your PR description to automatically link the PR to the relevant issue. 

## Code Review

- **JavaScript-Related Code:** All JavaScript-related code must be reviewed by @CaseyBramlett.
- **Other Code:** All other code must be reviewed by @IsaiahHarvi.

## Thread Resolution

- **Responsibility:** Threads in the PR should be resolved by the person who opened the thread, not the PR author.

## Merging PRs

- **Testing:** PRs should not be merged until all tests pass.
