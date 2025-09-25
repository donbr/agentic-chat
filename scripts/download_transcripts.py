#!/usr/bin/env python3
"""
YouTube Transcript Downloader

This script downloads transcripts from YouTube videos using yt-dlp.
It processes a list of video URLs and saves the transcripts as VTT files
in a specified output directory.

Part of the Agentic Chat Educational Content Generator project.
Licensed under MIT License - see LICENSE file for details.

Date: 2024-09-24
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Optional
import yt_dlp
from urllib.parse import urlparse, parse_qs


class YouTubeTranscriptDownloader:
    """
    A class for downloading YouTube video transcripts using yt-dlp.

    This class provides methods to download transcripts from YouTube videos,
    extract video IDs from URLs, and organize the downloaded files.
    """

    def __init__(self, output_dir: str = "transcripts", language: str = "en"):
        """
        Initialize the transcript downloader.

        Args:
            output_dir (str): Directory to save transcript files. Defaults to "transcripts".
            language (str): Language code for subtitles. Defaults to "en".
        """
        self.output_dir = Path(output_dir)
        self.language = language
        self.output_dir.mkdir(exist_ok=True)

        # Configure yt-dlp options
        self.ydl_opts = {
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': [language],
            'skip_download': True,
            'outtmpl': str(self.output_dir / '%(title)s_%(id)s.%(ext)s'),
            'quiet': False,
            'no_warnings': False,
        }

    def extract_video_id(self, url: str) -> Optional[str]:
        """
        Extract video ID from YouTube URL.

        Args:
            url (str): YouTube video URL

        Returns:
            Optional[str]: Video ID if found, None otherwise

        Examples:
            >>> downloader = YouTubeTranscriptDownloader()
            >>> downloader.extract_video_id("https://www.youtube.com/watch?v=t13Y5Igh66U")
            't13Y5Igh66U'
        """
        try:
            parsed_url = urlparse(url)

            # Standard YouTube URL format
            if parsed_url.netloc in ['www.youtube.com', 'youtube.com']:
                if '/watch' in parsed_url.path:
                    query_params = parse_qs(parsed_url.query)
                    return query_params.get('v', [None])[0]
                elif '/live/' in parsed_url.path:
                    # Handle live URLs
                    query_params = parse_qs(parsed_url.query)
                    return query_params.get('v', [None])[0]

            # Short YouTube URL format
            elif parsed_url.netloc == 'youtu.be':
                return parsed_url.path.lstrip('/')

        except Exception as e:
            print(f"Error extracting video ID from {url}: {e}")

        return None

    def download_transcript(self, url: str, custom_filename: Optional[str] = None) -> Dict[str, any]:
        """
        Download transcript for a single YouTube video.

        Args:
            url (str): YouTube video URL
            custom_filename (str, optional): Custom filename prefix. If None, uses video title.

        Returns:
            Dict[str, any]: Result dictionary containing success status, message, and file path
        """
        result = {
            'success': False,
            'url': url,
            'message': '',
            'file_path': None,
            'video_id': None
        }

        try:
            video_id = self.extract_video_id(url)
            result['video_id'] = video_id

            if not video_id:
                result['message'] = "Could not extract video ID from URL"
                return result

            # Update output template if custom filename provided
            if custom_filename:
                self.ydl_opts['outtmpl'] = str(self.output_dir / f'{custom_filename}_%(id)s.%(ext)s')
            else:
                self.ydl_opts['outtmpl'] = str(self.output_dir / '%(title)s_%(id)s.%(ext)s')

            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                # Get video info first
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'Unknown')

                print(f"Downloading transcript for: {title} ({video_id})")

                # Download subtitles
                ydl.download([url])

                # Find the downloaded transcript file
                expected_filename = custom_filename if custom_filename else title
                for file_path in self.output_dir.glob(f"*{video_id}*"):
                    if file_path.suffix in ['.vtt', '.srt']:
                        result['file_path'] = str(file_path)
                        break

                if result['file_path']:
                    result['success'] = True
                    result['message'] = f"Successfully downloaded transcript to {result['file_path']}"
                else:
                    result['message'] = "Transcript downloaded but file not found"

        except yt_dlp.DownloadError as e:
            if "no subtitles" in str(e).lower():
                result['message'] = "No subtitles available for this video"
            else:
                result['message'] = f"Download error: {str(e)}"
        except Exception as e:
            result['message'] = f"Unexpected error: {str(e)}"

        return result

    def download_multiple_transcripts(self, urls_with_names: List[tuple]) -> List[Dict[str, any]]:
        """
        Download transcripts for multiple YouTube videos.

        Args:
            urls_with_names (List[tuple]): List of tuples containing (url, custom_filename)

        Returns:
            List[Dict[str, any]]: List of result dictionaries for each download
        """
        results = []

        print(f"Starting download of {len(urls_with_names)} transcripts...")
        print(f"Output directory: {self.output_dir.absolute()}")
        print("-" * 60)

        for i, (url, custom_name) in enumerate(urls_with_names, 1):
            print(f"\n[{i}/{len(urls_with_names)}] Processing: {custom_name or 'Unknown'}")
            result = self.download_transcript(url, custom_name)
            results.append(result)

            if result['success']:
                print(f"✓ {result['message']}")
            else:
                print(f"✗ {result['message']}")

        return results

    def print_summary(self, results: List[Dict[str, any]]) -> None:
        """
        Print a summary of download results.

        Args:
            results (List[Dict[str, any]]): List of result dictionaries
        """
        print("\n" + "="*60)
        print("DOWNLOAD SUMMARY")
        print("="*60)

        successful = [r for r in results if r['success']]
        failed = [r for r in results if not r['success']]

        print(f"Total videos processed: {len(results)}")
        print(f"Successful downloads: {len(successful)}")
        print(f"Failed downloads: {len(failed)}")

        if successful:
            print("\n✓ Successful downloads:")
            for result in successful:
                print(f"  - {result['video_id']}: {os.path.basename(result['file_path'])}")

        if failed:
            print("\n✗ Failed downloads:")
            for result in failed:
                print(f"  - {result['video_id'] or 'Unknown'}: {result['message']}")


def main():
    """
    Main function to demonstrate the transcript downloader usage.
    """
    # Video URLs from the "How to Build ChatGPT" series
    video_urls = [
        ("https://www.youtube.com/live/OkqnAk1eH4M?si=9XJ0KcqMjR2ft6Fo", "part1"),
        ("https://www.youtube.com/live/BAtY88cw3rw?si=YBen_HcAfx89s3aE", "part2"),
        ("https://www.youtube.com/live/qQ6nCN6ynXo", "part3"),
        ("https://www.youtube.com/watch?v=t13Y5Igh66U", "part4"),
    ]

    # Create downloader instance
    downloader = YouTubeTranscriptDownloader(output_dir="transcripts", language="en")

    # Download all transcripts
    results = downloader.download_multiple_transcripts(video_urls)

    # Print summary
    downloader.print_summary(results)


if __name__ == "__main__":
    main()