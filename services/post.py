import requests


def upload_questions(json_data, api_url="http://localhost:8003/api/perguntas/"):
    results = []

    print(f"Uploading {len(json_data)} questions to {api_url}")

    for i, question in enumerate(json_data, 1):
        try:
            response = requests.post(api_url, json=question)

            if response.status_code == 200 or response.status_code == 201:
                result = response.json()
                results.append(result)
                print(
                    f"✅ Question {i}/{len(json_data)} uploaded successfully (ID: {result.get('id')})"
                )
            else:
                print(f"❌ Failed to upload question {i}/{len(json_data)}")
                print(f"Status code: {response.status_code}")
                print(f"Response: {response.text}")
        except Exception as e:
            print(f"❌ Error uploading question {i}/{len(json_data)}: {str(e)}")

    return results


def main(questions):
    api_url = input(
        "Enter API URL (press Enter for default http://localhost:8003/api/perguntas/): "
    )
    if not api_url:
        api_url = "http://localhost:8003/api/perguntas/"

    results = upload_questions(questions, api_url)

    print(
        f"\nUpload complete. {len(results)} out of {len(questions)} questions uploaded successfully."
    )


# questions = questions()
# main(questions)
