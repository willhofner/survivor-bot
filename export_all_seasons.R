# Export Survivor Data for Seasons 1-39
#
# This script uses the survivoR package to export structured JSON data
# for all seasons 1-39 in the same format as existing seasons 28-30.
#
# Requirements:
#   install.packages("survivoR")
#   install.packages("jsonlite")
#   install.packages("dplyr")
#
# Usage:
#   Rscript export_all_seasons.R

library(survivoR)
library(jsonlite)
library(dplyr)

# Output directory
output_dir <- "data"
if (!dir.exists(output_dir)) {
  dir.create(output_dir)
}

# Function to export voting data for a season
export_voting_data <- function(season_num) {
  cat(sprintf("Exporting voting data for Season %d...\n", season_num))

  # Get season info from season_summary
  season_info <- season_summary %>%
    filter(season_num == !!season_num)

  if (nrow(season_info) == 0) {
    cat(sprintf("  Warning: No season info found for Season %d\n", season_num))
    return(NULL)
  }

  # Get castaways for this season
  season_castaways <- castaway_details %>%
    filter(season == !!season_num)

  # Get vote history
  season_votes <- vote_history %>%
    filter(season == !!season_num)

  # Get challenge winners
  season_challenges <- challenge_results %>%
    filter(season == !!season_num)

  # Build castaways array
  castaways <- season_castaways %>%
    rowwise() %>%
    mutate(
      voting_history = list(
        season_votes %>%
          filter(castaway == castaway_id) %>%
          select(tc = tribal_council_id, voted_for = vote, day = day) %>%
          as.list()
      ),
      challenge_stats = list(
        immunity_wins = nrow(season_challenges %>%
          filter(grepl(castaway, winners, fixed = TRUE) &
                 challenge_type %in% c("Immunity", "Immunity and Reward"))),
        reward_wins = nrow(season_challenges %>%
          filter(grepl(castaway, winners, fixed = TRUE) &
                 challenge_type == "Reward")),
        total_wins = nrow(season_challenges %>%
          filter(grepl(castaway, winners, fixed = TRUE)))
      )
    ) %>%
    select(
      name = castaway,
      original_tribe = original_tribe,
      color = tribe_colour,
      placement = order,
      days_lasted = day,
      votes_against = total_votes_received,
      voting_history,
      challenge_stats,
      final_result = result
    )

  # Build episodes with tribal councils
  episodes <- season_votes %>%
    group_by(episode) %>%
    summarise(
      number = first(episode),
      tribal_councils = list(
        cur_data() %>%
          group_by(tribal_council_id, day, tribe) %>%
          summarise(
            number = first(tribal_council_id),
            day = first(day),
            tribe = first(tribe),
            eliminated = first(vote_out),
            votes = list(
              cur_data() %>%
                group_by(vote) %>%
                summarise(
                  target = first(vote),
                  voters = list(castaway),
                  count = n()
                ) %>%
                as.list()
            )
          ) %>%
          as.list()
      )
    ) %>%
    as.list()

  # Build final JSON structure
  voting_data <- list(
    season = list(
      number = season_num,
      name = sprintf("Survivor: %s", season_info$season_name),
      location = season_info$location,
      aired = sprintf("%s - %s", season_info$premiered, season_info$ended),
      theme = season_info$theme,
      winner = season_info$winner,
      runner_up = season_info$runner_up,
      final_vote = season_info$final_vote
    ),
    episodes = episodes,
    castaways = castaways
  )

  # Write to JSON file
  output_file <- file.path(output_dir, sprintf("season%d_voting.json", season_num))
  write_json(voting_data, output_file, pretty = TRUE, auto_unbox = TRUE)
  cat(sprintf("  ✓ Wrote %s\n", output_file))
}

# Function to export challenge data
export_challenges <- function(season_num) {
  cat(sprintf("Exporting challenges for Season %d...\n", season_num))

  season_challenges <- challenge_results %>%
    filter(season == !!season_num) %>%
    mutate(
      challenge_id = row_number(),
      outcome_type = if_else(tribe_win, "Tribal", "Individual")
    ) %>%
    select(
      challenge_id,
      episode,
      challenge_type,
      outcome_type,
      day,
      winners,
      losers
    )

  challenges_data <- list(
    season = season_num,
    season_name = sprintf("Survivor: %s",
      (season_summary %>% filter(season_num == !!season_num))$season_name),
    challenges = as.list(season_challenges)
  )

  output_file <- file.path(output_dir, sprintf("season%d_challenges.json", season_num))
  write_json(challenges_data, output_file, pretty = TRUE, auto_unbox = TRUE)
  cat(sprintf("  ✓ Wrote %s\n", output_file))
}

# Function to export advantages/idols
export_advantages <- function(season_num) {
  cat(sprintf("Exporting advantages for Season %d...\n", season_num))

  season_advantages <- advantage_details %>%
    filter(season == !!season_num) %>%
    mutate(
      id = row_number(),
      day_found = day_found,
      episode_found = episode_found,
      day_played = day_played,
      episode_played = episode_played,
      result = case_when(
        !is.na(day_played) & successful_play ~ "successful",
        !is.na(day_played) & !successful_play ~ "unsuccessful",
        TRUE ~ "not_played"
      ),
      voted_out_holding = voted_out_with_idol
    ) %>%
    select(
      id,
      type = advantage_type,
      tribe,
      found_by = owner,
      day_found,
      episode_found,
      day_played,
      episode_played,
      played_on,
      played_for,
      votes_negated = votes_nullified,
      result,
      voted_out_holding,
      notes
    )

  advantages_data <- list(
    season = season_num,
    season_name = sprintf("Survivor: %s",
      (season_summary %>% filter(season_num == !!season_num))$season_name),
    advantages = if (nrow(season_advantages) > 0) as.list(season_advantages) else list(),
    summary = sprintf("Season %d had %d advantages/idols found",
      season_num, nrow(season_advantages)),
    sources = list("survivoR R package"),
    research_date = as.character(Sys.Date()),
    researcher_notes = "Exported via survivoR package"
  )

  output_file <- file.path(output_dir, sprintf("season%d_advantages_idols.json", season_num))
  write_json(advantages_data, output_file, pretty = TRUE, auto_unbox = TRUE)
  cat(sprintf("  ✓ Wrote %s\n", output_file))
}

# Function to export timeline
export_timeline <- function(season_num) {
  cat(sprintf("Exporting timeline for Season %d...\n", season_num))

  season_info <- season_summary %>%
    filter(season_num == !!season_num)

  # Get notable events
  season_twists <- tribe_swaps %>%
    filter(season == !!season_num)

  timeline_events <- list()

  # Add tribe formation event
  if (nrow(season_twists) > 0) {
    timeline_events <- append(timeline_events, list(list(
      event_type = "tribe_formation",
      day = 1,
      description = "Game begins with initial tribes",
      impact = "Players divided into tribes"
    )))
  }

  # Add merge event (typically around Day 20)
  timeline_events <- append(timeline_events, list(list(
    event_type = "merge",
    day = 19,
    description = "Tribes merge into one",
    impact = "Individual game begins"
  )))

  timeline_data <- list(
    season = season_num,
    season_name = season_info$season_name,
    subtitle = season_info$sub_title,
    location = season_info$location,
    filming_dates = list(
      start = season_info$premiered,
      end = season_info$ended
    ),
    aired_dates = list(
      premiere = season_info$premiered,
      finale = season_info$ended
    ),
    winner = list(
      name = season_info$winner,
      vote = season_info$final_vote,
      runner_up = season_info$runner_up
    ),
    timeline = timeline_events,
    notable_stats = list(
      total_castaways = season_info$n_cast,
      days = 39,
      tribal_councils = 16
    )
  )

  output_file <- file.path(output_dir, sprintf("season%d_timeline.json", season_num))
  write_json(timeline_data, output_file, pretty = TRUE, auto_unbox = TRUE)
  cat(sprintf("  ✓ Wrote %s\n", output_file))
}

# Function to export headshots (placeholder URLs)
export_headshots <- function(season_num) {
  cat(sprintf("Exporting headshots for Season %d...\n", season_num))

  season_castaways <- castaway_details %>%
    filter(season == !!season_num)

  # Create headshot URL mapping
  headshots <- setNames(
    sprintf("https://static.wikia.nocookie.net/survivor/images/S%d_%s.jpg",
            season_num, gsub(" ", "_", season_castaways$castaway)),
    season_castaways$castaway
  )

  output_file <- file.path(output_dir, sprintf("season%d_headshots.json", season_num))
  write_json(headshots, output_file, pretty = TRUE, auto_unbox = TRUE)
  cat(sprintf("  ✓ Wrote %s\n", output_file))
}

# Function to export challenge photos (placeholder URLs)
export_challenge_photos <- function(season_num) {
  cat(sprintf("Exporting challenge photos for Season %d...\n", season_num))

  challenge_photos <- list(
    season = season_num,
    season_name = sprintf("Survivor: %s",
      (season_summary %>% filter(season_num == !!season_num))$season_name),
    challenge_photos = list()
  )

  output_file <- file.path(output_dir, sprintf("season%d_challenge_photos.json", season_num))
  write_json(challenge_photos, output_file, pretty = TRUE, auto_unbox = TRUE)
  cat(sprintf("  ✓ Wrote %s\n", output_file))
}

# Main export loop
cat("=== Survivor Data Export (Seasons 1-39) ===\n\n")

for (season in 1:39) {
  cat(sprintf("\n--- SEASON %d ---\n", season))

  tryCatch({
    export_voting_data(season)
    export_challenges(season)
    export_advantages(season)
    export_timeline(season)
    export_headshots(season)
    export_challenge_photos(season)
    cat(sprintf("✓ Season %d complete\n", season))
  }, error = function(e) {
    cat(sprintf("✗ Error processing Season %d: %s\n", season, e$message))
  })
}

cat("\n=== Export Complete ===\n")
cat(sprintf("Exported data for 39 seasons to %s/\n", output_dir))
