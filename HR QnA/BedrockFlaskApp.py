from flask import Flask, request, jsonify
from flask_cors import CORS
from botocore.exceptions import ClientError
import boto3
import mysql.connector
from mysql.connector import Error
from pytz import timezone
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


class BedRockClient:
    def __init__(self, region_name="ap-south-1"):
        self.region_name = region_name

    def return_runtime_client(self, run_time=True):
        if run_time:
            bedrock_client = boto3.client(
                service_name="bedrock-agent-runtime",
                region_name=self.region_name)
        else:
            bedrock_client = boto3.client(
                service_name="bedrock-agent",
                region_name=self.region_name)
        return bedrock_client

    def invoke_bedrock_agent(self, agent_id, agent_alias_id, session_id, prompt=None):
        completion = ""
        traces = []
        try:
            bedrock_client = self.return_runtime_client(run_time=True)
            response = bedrock_client.invoke_agent(
                agentId=agent_id,
                agentAliasId=agent_alias_id,
                sessionId=session_id,
                inputText=prompt,
            )
            for event in response.get("completion"):
                try:
                    trace = event["trace"]
                    traces.append(trace['trace'])
                except KeyError:
                    chunk = event["chunk"]
                    completion = completion + chunk["bytes"].decode()
                except Exception as e:
                    print(e)
        except ClientError as e:
            print(e)
        return completion, traces


bedrock_client = BedRockClient()


@app.route('/invoke_agent', methods=['POST'])
def invoke_agent():
    data = request.get_json()
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({"error": "Missing required parameter: prompt"}), 400

    try:
        response, traces = bedrock_client.invoke_bedrock_agent(
            agent_id="GXLYSVDBSQ",
            agent_alias_id="BJ6TFUTWS8",  # Ensure this is a string
            session_id="123",
            prompt=prompt
        )
        # print(prompt)
        # print(response)
        return jsonify({"response": response}), 200
        # , "traces": traces
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# MySQL configuration
mysql_config = {
    'host': 'localhost',
    'database': 'CDL',
    'user': 'root',
    'password': 'Amod@0511',
    'autocommit': True
}


def get_ist_timestamp():
    ist = timezone('Asia/Kolkata')
    return datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S')


@app.route('/store_interaction', methods=['POST'])
def store_interaction():
    data = request.get_json()
    user_name = data.get('userName')
    prompt = data.get('prompt')
    response = data.get('response')
    timestamp = get_ist_timestamp()

    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()

        # Insert data into chatbot_interactions table
        sql_query = """
        INSERT INTO chatbot_interactions (user_name, prompt, response, timestamp)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql_query, (user_name, prompt, response, timestamp))
        interaction_id = cursor.lastrowid

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({'message': 'Interaction stored successfully', 'interaction_id': interaction_id}), 200

    except Error as e:
        print(f"Error storing interaction: {e}")
        return jsonify({'message': 'Error storing interaction'}), 500
    except Exception as e:
        print(f"Exception: {e}")
        return jsonify({'message': 'Server error'}), 500


@app.route('/store_feedback', methods=['POST'])
def store_feedback():
    data = request.get_json()
    interaction_id = data.get('interactionId')
    feedback = data.get('feedback')

    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()

        # Update feedback column in chatbot_interactions table
        sql_query = """
        UPDATE chatbot_interactions
        SET feedback = %s
        WHERE id = %s
        """
        cursor.execute(sql_query, (feedback, interaction_id))

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({'message': 'Feedback stored and linked successfully'}), 200

    except Error as e:
        print(f"Error storing feedback: {e}")
        return jsonify({'message': 'Error storing feedback'}), 500
    except Exception as e:
        print(f"Exception: {e}")
        return jsonify({'message': 'Server error'}), 500


if __name__ == '__main__':
    app.run(debug=True)
