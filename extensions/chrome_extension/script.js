"use strict";
/*jshint esversion: 9 */
/* jshint -W097 */

// default url where report server is located
const quality_change_url = "http://localhost:34543/quality";
const state_change_url = "http://localhost:34543/state";
const stats_url = "http://localhost:34543/report";
const report_time = 200;

function postReport(url, jsonData) {
    // this function sends json data to report server
    let xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json; charset=utf-8");
    xhr.send(JSON.stringify(jsonData));
}

function onStateChange(event) {
    // this function catch player state changes and report them
    postReport(
        state_change_url,
        {
            fraction: player.getVideoLoadedFraction(),
            current_time: player.getCurrentTime(),
            new_state: event,
        }
    );
}

function onPlaybackQualityChange(event) {
    // this function post quality changes
    postReport(
        quality_change_url,
        {
            fraction: player.getVideoLoadedFraction(),
            current_time: player.getCurrentTime(),
            new_quality: event,
        }
    );
}

function sendStats() {
    // this function is executed every X ms and reports current statistics
    let stats_for_nerds = player.getStatsForNerds();

    let [video_id, scpn] = stats_for_nerds.video_id_and_cpn.split("/").map(x => x.trim());

    function parseDims(resolution, splitter) {
        let width, height, framerate;
        resolution = resolution.split(splitter);
        framerate = parseFloat(resolution[1]);
        [width, height] = resolution[0].split("x").map(x => parseInt(x));
        return [width, height, framerate];
    }

    let [current_resolution, optimal_resolution] = stats_for_nerds.resolution.split("/").map(x => x.trim());
    let [current_height, current_width, current_framerate] = parseDims(current_resolution, "@");
    let [optimal_height, optimal_width, optimal_framerate] = parseDims(optimal_resolution, "@");

    let [viewport_width, viewport_height, viewport_scale_factor] = parseDims(
        stats_for_nerds.dims_and_frames.split("/")[0],
        "*"
    );
    let [frames_dropped, frames_total] = stats_for_nerds
        .dims_and_frames
        .split("/")[1]
        .trim()
        .split(" dropped of ")
        .map(x => parseInt(x));

    let [video_codec, audio_codec] = stats_for_nerds.codecs.split("/").map(x => x.trim());
    let bandwidth_kbps = parseInt(stats_for_nerds.bandwidth_kbps.split(" ")[0]);
    let buffer_health_seconds = parseFloat(stats_for_nerds.buffer_health_seconds.split(" ")[0]);
    let date = stats_for_nerds.date;
    let debug_info = stats_for_nerds.debug_info;
    let network_activity_kbytes = parseInt(stats_for_nerds.network_activity_bytes.split(" ")[0]);
    let playback_fraction = player.getVideoLoadedFraction();
    let current_time = player.getCurrentTime();

    postReport(
        stats_url,
        {
            video_id: video_id,  // unique video id
            scpn: scpn,  // unique playback id - this would be different for 2 playbacks of the same video
            current_resolution: {  // current resolution of the video
                width: current_width,
                height: current_height,
                framerate: current_framerate
            },
            optimal_resolution: {  // optimal resolution of the video by YouTube estimation
                width: optimal_width,
                height: optimal_height,
                framerate: optimal_framerate
            },
            viewport: {  // current dims of the player in the browser
                width: viewport_width,
                height: viewport_height,
                scale_factor: viewport_scale_factor  // some scale factor?
            },
            frames_dropped: frames_dropped, // how many frames dropped
            frames_total: frames_total,     // total frames played
            video_codec: video_codec,       // video codec used
            audio_codec: audio_codec,        // audio codec used
            bandwidth_estimation_kbps: bandwidth_kbps,  // bandwidth estimation of YouTube
            buffer_health_seconds: buffer_health_seconds,   // how many seconds video can play without downloading new chunk
            date: date,     // current date
            debug_info: debug_info,     // contains s: status, t: time, b: buffer in seconds, and also letters P (paused?) and L (??)
                                        // also see https://www.reddit.com/r/youtube/comments/bi0s7s/mistery_text_in_nerd_stats/elxw913/?context=3
            network_activity_kbytes: network_activity_kbytes,
            playback_fraction: playback_fraction,   // portion of video that is already played
            current_time: current_time,             // elapsed time in seconds since the video start
        });
}

// wait until player is ready
while (!document.getElementById("movie_player")) {
    (async () => {
        await new Promise(r => setTimeout(r, 500));
    })();
}

// get the player
let player = document.getElementById("movie_player");

// register callbacks on state and quality changes
player.addEventListener("onStateChange", onStateChange);
player.addEventListener("onPlaybackQualityChange", onPlaybackQualityChange);

// report stats for nerds every X ms
setInterval(sendStats, report_time);
